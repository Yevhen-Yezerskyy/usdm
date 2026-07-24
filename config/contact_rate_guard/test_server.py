import unittest
from unittest.mock import patch

from server import BAN_SECONDS, Guard


class GuardTests(unittest.TestCase):
    def test_third_event_in_twenty_seconds_bans_for_a_day(self):
        guard = Guard()
        self.assertEqual(guard.check("nginx", "site.test", "192.0.2.1", 100), (True, 0))
        self.assertEqual(guard.check("nginx", "site.test", "192.0.2.1", 105), (True, 0))
        self.assertEqual(guard.check("nginx", "site.test", "192.0.2.1", 110), (False, BAN_SECONDS))

    def test_layers_and_hosts_are_isolated(self):
        guard = Guard()
        for now in (100, 101):
            self.assertEqual(guard.check("nginx", "one.test", "192.0.2.1", now), (True, 0))
        self.assertEqual(guard.check("django", "one.test", "192.0.2.1", 102), (True, 0))
        self.assertEqual(guard.check("nginx", "two.test", "192.0.2.1", 102), (True, 0))

    def test_expired_events_no_longer_count(self):
        guard = Guard()
        self.assertEqual(guard.check("django", "site.test", "192.0.2.1", 100), (True, 0))
        self.assertEqual(guard.check("django", "site.test", "192.0.2.1", 105), (True, 0))
        self.assertEqual(guard.check("django", "site.test", "192.0.2.1", 126), (True, 0))

    def test_capacity_exhaustion_is_bounded_and_fail_open(self):
        guard = Guard()
        with patch("server.MAX_KEYS", 1):
            guard.check("nginx", "one.test", "192.0.2.1", 100)
            self.assertEqual(guard.check("nginx", "two.test", "192.0.2.2", 101), (True, 0))
            self.assertEqual(len(guard.last_seen), 1)


if __name__ == "__main__":
    unittest.main()
