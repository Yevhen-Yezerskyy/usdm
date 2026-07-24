#!/usr/bin/env python3
"""Small best-effort, RAM-only rate guard for the public contact form."""

from collections import defaultdict, deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Lock
import json
import os
import time


FORM_PATHS = {"/uk/contact/send/", "/de/contact/send/"}
WINDOWS = ((20, 2), (60, 5), (120, 10), (15 * 60, 10), (60 * 60, 20))
BAN_SECONDS = 24 * 60 * 60
MAX_KEYS = int(os.environ.get("RATE_GUARD_MAX_KEYS", "10000"))
PORT = int(os.environ.get("RATE_GUARD_PORT", "8080"))


class Guard:
    def __init__(self):
        self.events = defaultdict(deque)
        self.bans = {}
        self.last_seen = {}
        self.lock = Lock()

    def check(self, layer, site, ip, now=None):
        now = time.monotonic() if now is None else now
        key = (layer[:16], site[:255].lower(), ip[:64])
        with self.lock:
            if key not in self.last_seen and len(self.last_seen) >= MAX_KEYS:
                self._prune(now)
                if len(self.last_seen) >= MAX_KEYS:
                    return True, 0

            banned_until = self.bans.get(key, 0)
            if banned_until > now:
                self.last_seen[key] = now
                return False, max(1, int(banned_until - now))
            self.bans.pop(key, None)

            events = self.events[key]
            oldest_allowed = now - WINDOWS[-1][0]
            while events and events[0] <= oldest_allowed:
                events.popleft()
            events.append(now)
            self.last_seen[key] = now

            for window, limit in WINDOWS:
                count = sum(event > now - window for event in events)
                if count > limit:
                    self.bans[key] = now + BAN_SECONDS
                    events.clear()
                    self._prune(now)
                    return False, BAN_SECONDS

            self._prune(now)
            return True, 0

    def _prune(self, now):
        stale_before = now - WINDOWS[-1][0]
        stale = [
            key
            for key, seen in self.last_seen.items()
            if seen <= stale_before and self.bans.get(key, 0) <= now
        ]
        for key in stale:
            self.events.pop(key, None)
            self.bans.pop(key, None)
            self.last_seen.pop(key, None)

        excess = len(self.last_seen) - MAX_KEYS
        if excess > 0:
            removable = sorted(
                (seen, key)
                for key, seen in self.last_seen.items()
                if self.bans.get(key, 0) <= now
            )
            for _, key in removable[:excess]:
                self.events.pop(key, None)
                self.bans.pop(key, None)
                self.last_seen.pop(key, None)


guard = Guard()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self._reply(200, {"status": "ok"})
        else:
            self._reply(404, {"detail": "not found"})

    def do_POST(self):
        if self.path != "/check":
            self._reply(404, {"detail": "not found"})
            return

        method = self.headers.get("X-Original-Method", "")
        path = (
            self.headers.get("X-Original-Path")
            or self.headers.get("X-Original-URI", "")
        ).split("?", 1)[0]
        if method != "POST" or path not in FORM_PATHS:
            self._reply(204)
            return

        allowed, retry_after = guard.check(
            self.headers.get("X-Guard-Layer") or self.headers.get("X-Rate-Layer", "unknown"),
            self.headers.get("X-Guard-Site") or self.headers.get("X-Rate-Site", "unknown"),
            self.headers.get("X-Real-IP", "unknown"),
        )
        if allowed:
            self._reply(204)
            return

        # auth_request understands a 401 and nginx maps it to public 429.
        layer = self.headers.get("X-Guard-Layer") or self.headers.get("X-Rate-Layer", "")
        status = 401 if layer == "nginx" else 429
        self._reply(status, {"detail": "rate limited"}, {"Retry-After": str(retry_after)})

    def _reply(self, status, payload=None, headers=None):
        body = b"" if payload is None else json.dumps(payload, separators=(",", ":")).encode()
        self._last_status = status
        self.send_response(status)
        if body:
            self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        for name, value in (headers or {}).items():
            self.send_header(name, value)
        self.end_headers()
        if body:
            self.wfile.write(body)

    def log_message(self, format, *args):
        if getattr(self, "_last_status", None) not in {200, 204}:
            super().log_message(format, *args)


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
