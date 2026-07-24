
from __future__ import annotations

import re


class TextSplitter:

    def __init__(self):
        pass

    # --------------------------------------------------

    def split(
        self,
        text: str,
        chunk_size: int,
        overlap: int,
    ) -> list[str]:
        """
        Split text into overlapping chunks.

        Parameters
        ----------
        text : str
            Document text

        chunk_size : int
            Maximum characters per chunk

        overlap : int
            Number of overlapping characters

        Returns
        -------
        list[str]
        """

        if not text:
            return []

        # Normalize whitespace
        text = text.replace("\r\n", "\n")
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"[ \t]+", " ", text)

        paragraphs = [
            p.strip()
            for p in text.split("\n\n")
            if p.strip()
        ]

        chunks = []
        current_chunk = ""

        for paragraph in paragraphs:

            # Paragraph fits
            if len(current_chunk) + len(paragraph) + 2 <= chunk_size:

                if current_chunk:
                    current_chunk += "\n\n"

                current_chunk += paragraph

            else:

                if current_chunk:
                    chunks.append(current_chunk)

                # Large paragraph
                if len(paragraph) > chunk_size:

                    chunks.extend(
                        self._split_large_paragraph(
                            paragraph,
                            chunk_size,
                            overlap,
                        )
                    )

                    current_chunk = ""

                else:

                    current_chunk = paragraph

        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    # --------------------------------------------------

    def _split_large_paragraph(
        self,
        paragraph: str,
        chunk_size: int,
        overlap: int,
    ) -> list[str]:

        chunks = []

        start = 0

        while start < len(paragraph):

            end = start + chunk_size

            if end >= len(paragraph):
                chunks.append(paragraph[start:])
                break

            split_point = paragraph.rfind(".", start, end)

            if split_point == -1:
                split_point = paragraph.rfind(" ", start, end)

            if split_point == -1:
                split_point = end

            chunk = paragraph[start:split_point].strip()

            if chunk:
                chunks.append(chunk)

            start = max(
                split_point - overlap,
                start + 1,
            )

        return chunks

    # --------------------------------------------------

    def chunk_count(
        self,
        text: str,
        chunk_size: int,
        overlap: int,
    ) -> int:

        return len(
            self.split(
                text=text,
                chunk_size=chunk_size,
                overlap=overlap,
            )
        )