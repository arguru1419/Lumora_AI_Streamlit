
from __future__ import annotations

import time
from collections import defaultdict


class RateLimiter:

    def __init__(
        self,
        max_requests: int = 30,
        window_seconds: int = 60,
    ):
        """
        Parameters
        ----------
        max_requests:
            Maximum requests allowed.

        window_seconds:
            Time window in seconds.
        """

        self.max_requests = max_requests
        self.window_seconds = window_seconds

        self.requests = defaultdict(list)

    def allow(self, session_id: str) -> bool:
        """
        Returns True if request is allowed.
        """

        now = time.time()

        timestamps = self.requests[session_id]

        # Remove expired timestamps
        timestamps[:] = [
            ts
            for ts in timestamps
            if now - ts < self.window_seconds
        ]

        if len(timestamps) >= self.max_requests:
            return False

        timestamps.append(now)

        return True

    def remaining_requests(
        self,
        session_id: str,
    ) -> int:

        now = time.time()

        timestamps = self.requests[session_id]

        timestamps[:] = [
            ts
            for ts in timestamps
            if now - ts < self.window_seconds
        ]

        return self.max_requests - len(timestamps)

    def reset(self, session_id: str):
        """
        Clear rate limit history for one session.
        """

        if session_id in self.requests:
            del self.requests[session_id]

    def reset_all(self):
        """
        Clear all rate limits.
        """

        self.requests.clear()