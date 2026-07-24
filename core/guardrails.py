
from __future__ import annotations

import re


class GuardRails:

    def __init__(self):

        self.max_prompt_length = 5000

        self.blocked_patterns = [

            # Prompt injection
            r"ignore\s+previous\s+instructions",
            r"ignore\s+all\s+instructions",
            r"forget\s+everything",
            r"system\s+prompt",
            r"developer\s+message",
            r"reveal\s+your\s+prompt",
            r"show\s+hidden\s+instructions",

            # Jailbreak attempts
            r"bypass",
            r"jailbreak",
            r"disable\s+safety",
            r"disable\s+guardrails",

            # Dangerous code generation
            r"rm\s+-rf",
            r"del\s+/f",
            r"format\s+c:",
            r"shutdown\s+/s",

            # Script injection
            r"<script.*?>",
            r"</script>",
        ]

    def _normalize(self, text: str) -> str:
        return text.lower().strip()

    def validate(self, prompt: str) -> bool:
        """
        Returns True if the prompt is safe.
        """

        if not prompt:
            return False

        prompt = self._normalize(prompt)

        if len(prompt) > self.max_prompt_length:
            return False

        for pattern in self.blocked_patterns:
            if re.search(pattern, prompt):
                return False

        return True

    def check(self, prompt: str):
        """
        Returns (is_safe, message)
        """

        if not prompt:
            return False, "Prompt is empty."

        if len(prompt) > self.max_prompt_length:
            return (
                False,
                f"Prompt exceeds {self.max_prompt_length} characters."
            )

        normalized = self._normalize(prompt)

        for pattern in self.blocked_patterns:
            if re.search(pattern, normalized):
                return (
                    False,
                    "Prompt blocked by safety guardrails."
                )

        return True, "Prompt accepted."