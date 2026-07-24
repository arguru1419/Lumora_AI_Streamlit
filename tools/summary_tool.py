
from __future__ import annotations


class SummaryTool:

    name = "summary"

    def execute(
        self,
        text: str,
        max_sentences: int = 3,
    ) -> str:

        if not text.strip():
            return "Nothing to summarize."

        sentences = text.replace("\n", " ").split(".")

        cleaned = [
            sentence.strip()
            for sentence in sentences
            if sentence.strip()
        ]

        summary = ". ".join(cleaned[:max_sentences])

        if summary:
            summary += "."

        return summary