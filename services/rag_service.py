
from __future__ import annotations

import os

import config
from services.document_loader import DocumentLoader
from services.text_splitter import TextSplitter


class RAGService:

    def __init__(self):

        self.loader = DocumentLoader()
        self.splitter = TextSplitter()

        # Stores document chunks in memory.
        # Can later be replaced with ChromaDB/FAISS
        self.documents = []

    # --------------------------------------------------

    def ingest_document(self, file_path: str):
        """
        Load a document and split it into chunks.
        """

        if not os.path.exists(file_path):
            raise FileNotFoundError(file_path)

        text = self.loader.load(file_path)

        chunks = self.splitter.split(
            text=text,
            chunk_size=config.CHUNK_SIZE,
            overlap=config.CHUNK_OVERLAP,
        )

        for chunk in chunks:

            self.documents.append(
                {
                    "text": chunk,
                    "source": os.path.basename(file_path),
                }
            )

        return len(chunks)

    # --------------------------------------------------

    def retrieve(
        self,
        query: str,
    ) -> str:
        """
        Retrieve the most relevant chunks.

        Current implementation:
        Keyword-overlap retrieval.

        Future implementation:
        ChromaDB semantic search.
        """

        if not self.documents:
            return ""

        query_words = set(query.lower().split())

        scored = []

        for document in self.documents:

            text = document["text"]

            score = len(
                query_words.intersection(
                    set(text.lower().split())
                )
            )

            scored.append(
                (
                    score,
                    text,
                )
            )

        scored.sort(
            key=lambda x: x[0],
            reverse=True,
        )

        top_chunks = [
            chunk
            for score, chunk in scored[: config.TOP_K]
            if score > 0
        ]

        return "\n\n".join(top_chunks)

    # --------------------------------------------------

    def clear(self):
        """
        Remove all indexed documents.
        """

        self.documents.clear()

    # --------------------------------------------------

    def document_count(self):

        return len(self.documents)