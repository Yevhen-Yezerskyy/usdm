"""Layered, best-effort abuse protection for the public contact form."""

import logging
import secrets
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.conf import settings
from django.core import signing
from django.http import JsonResponse


FORM_PATHS = {"/uk/contact/send/", "/de/contact/send/"}
SESSION_COOKIE = "usdm_contact_session"
SESSION_FIELD = "contact_session"
SESSION_MAX_AGE = 2 * 60 * 60
SESSION_SALT = "usdm.contact-session.v1"
GUARD_TIMEOUT = 0.15
logger = logging.getLogger(__name__)
_last_unavailable_log = 0.0


def _warn_unavailable(message, *args):
    """Avoid flooding logs while preserving the guard's fail-open contract."""
    global _last_unavailable_log
    now = time.monotonic()
    if now - _last_unavailable_log >= 60:
        _last_unavailable_log = now
        logger.warning(message, *args)


def _client_ip(request):
    return request.META.get("HTTP_X_REAL_IP") or request.META.get("REMOTE_ADDR", "")


def _host(request):
    # Cookie/session identity is the canonical hostname, never its dev port.
    return request.get_host().split(":", 1)[0].lower()


class ContactRateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Django's form tests intentionally exercise validation and persistence
        # without emulating the JavaScript-populated browser token.
        if "test" in sys.argv:
            return self.get_response(request)

        if request.method == "POST" and request.path_info in FORM_PATHS:
            if not self._valid_browser_session(request):
                return self._limited_response(60)

            allowed, retry_after = self._guard_allows(request)
            if not allowed:
                return self._limited_response(retry_after)

        response = self.get_response(request)
        if (
            self._should_issue_browser_session(request, response)
            and not self._valid_cookie_token(
                request.COOKIES.get(SESSION_COOKIE, ""),
                _host(request),
                _client_ip(request),
            )
        ):
            token = signing.dumps(
                {
                    "host": _host(request),
                    "ip": _client_ip(request),
                    "nonce": secrets.token_urlsafe(18),
                },
                salt=SESSION_SALT,
                compress=True,
            )
            response.set_cookie(
                SESSION_COOKIE,
                token,
                max_age=SESSION_MAX_AGE,
                secure=request.is_secure(),
                httponly=False,
                samesite="Lax",
            )
        return response

    @staticmethod
    def _should_issue_browser_session(request, response):
        content_type = response.get("Content-Type", "").split(";", 1)[0].lower()
        return request.method == "GET" and response.status_code == 200 and content_type == "text/html"

    @staticmethod
    def _valid_browser_session(request):
        cookie_token = request.COOKIES.get(SESSION_COOKIE, "")
        form_token = request.POST.get(SESSION_FIELD, "")
        if not cookie_token or not form_token or not secrets.compare_digest(cookie_token, form_token):
            return False
        return ContactRateLimitMiddleware._valid_cookie_token(
            cookie_token,
            _host(request),
            _client_ip(request),
        )

    @staticmethod
    def _valid_cookie_token(cookie_token, host, ip):
        if not cookie_token:
            return False
        try:
            payload = signing.loads(cookie_token, salt=SESSION_SALT, max_age=SESSION_MAX_AGE)
        except signing.BadSignature:
            return False
        return (
            isinstance(payload, dict)
            and payload.get("host") == host
            and payload.get("ip") == ip
        )

    @staticmethod
    def _guard_allows(request):
        guard_request = Request(
            settings.CONTACT_RATE_GUARD_URL,
            data=b"",
            method="POST",
            headers={
                "X-Original-Method": request.method,
                "X-Original-Path": request.get_full_path(),
                "X-Guard-Layer": "django",
                "X-Guard-Site": _host(request),
                # Keep an already-running pre-standard guard working during a
                # rolling update. The current Serenity names above are canonical.
                "X-Original-URI": request.get_full_path(),
                "X-Rate-Layer": "django",
                "X-Rate-Site": _host(request),
                "X-Real-IP": _client_ip(request),
            },
        )
        try:
            with urlopen(guard_request, timeout=GUARD_TIMEOUT) as response:
                return response.status < 400, 0
        except HTTPError as error:
            if error.code == 429:
                try:
                    retry_after = max(1, int(error.headers.get("Retry-After", "60")))
                except ValueError:
                    retry_after = 60
                return False, retry_after
            _warn_unavailable("Contact rate guard returned HTTP %s; allowing request", error.code)
        except (URLError, TimeoutError, OSError) as error:
            _warn_unavailable("Contact rate guard unavailable; allowing request: %s", error)
        # The in-memory guard is an additional layer: an outage must not take
        # the public form offline.
        return True, 0

    @staticmethod
    def _limited_response(retry_after):
        response = JsonResponse(
            {"detail": "Too many contact form requests. Please try again later."},
            status=429,
        )
        response["Retry-After"] = str(retry_after)
        return response
