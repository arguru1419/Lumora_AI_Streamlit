"""
tools.py

Simple Tool Router

Each tool performs a dedicated task.
"""

from typing import List


class Tools:

    @staticmethod
    def summarize(chunks: List[str]) -> str:
        """
        Create a short summary from document chunks.
        """

        if not chunks:
            return "No document has been uploaded."

        text = " ".join(chunks[:5])

        if len(text) > 1200:
            text = text[:1200]

        prompt = f"""
Summarize the following document in 5 bullet points.

{text}
"""

        return prompt

    # -----------------------------------------

    @staticmethod
    def document_statistics(chunks: List[str]):

        words = sum(
            len(chunk.split())
            for chunk in chunks
        )

        return {

            "Chunks": len(chunks),
            "Words": words

        }

    # -----------------------------------------

    @staticmethod
    def requires_summary(question: str):

        keywords = [

            "summary",
            "summarize",
            "overview",
            "brief"

        ]

        q = question.lower()

        return any(
            word in q
            for word in keywords
        )