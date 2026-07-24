
from __future__ import annotations

from pathlib import Path

import fitz  # PyMuPDF
from docx import Document


class DocumentLoader:

    def __init__(self):
        self.supported_extensions = {
            ".pdf",
            ".docx",
            ".txt",
        }

    # --------------------------------------------------

    def load(self, file_path: str) -> str:
        """
        Load document based on extension.
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(path)

        extension = path.suffix.lower()

        if extension not in self.supported_extensions:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        if extension == ".pdf":
            return self._load_pdf(path)

        if extension == ".docx":
            return self._load_docx(path)

        if extension == ".txt":
            return self._load_txt(path)

        return ""

    # --------------------------------------------------

    def _load_pdf(self, path: Path) -> str:

        text = []

        document = fitz.open(path)

        try:

            for page in document:

                page_text = page.get_text("text")

                if page_text:
                    text.append(page_text)

        finally:
            document.close()

        return "\n".join(text).strip()

    # --------------------------------------------------

    def _load_docx(self, path: Path) -> str:

        document = Document(path)

        paragraphs = []

        for paragraph in document.paragraphs:

            value = paragraph.text.strip()

            if value:
                paragraphs.append(value)

        return "\n".join(paragraphs)

    # --------------------------------------------------

    def _load_txt(self, path: Path) -> str:

        with open(
            path,
            "r",
            encoding="utf-8",
            errors="ignore",
        ) as file:

            return file.read().strip()