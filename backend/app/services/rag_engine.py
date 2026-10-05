from __future__ import annotations

import json
import pickle
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

import numpy as np
from sentence_transformers import SentenceTransformer

from config import (
    EMBEDDING_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    TOP_K,
    INDEX_DIR,
)


@dataclass
class Chunk:
    id: str
    text: str
    conversation_id: str
    platform: str
    role: str
    message_ids: list[int]


class ConversationRAG:
    """Small, local RAG engine for Inbox AI.

    Pipeline:
        JSON conversations
            -> normalized text
            -> overlapping chunks
            -> sentence embeddings
            -> cosine similarity
            -> top-k context retrieval
    """

    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.chunks: list[Chunk] = []
        self.embeddings: np.ndarray | None = None
        self._load_index()

    def _load_index(self):
        metadata_file = INDEX_DIR / "chunks.pkl"
        embeddings_file = INDEX_DIR / "embeddings.npy"

        if metadata_file.exists() and embeddings_file.exists():
            with metadata_file.open("rb") as f:
                raw = pickle.load(f)
            self.chunks = [Chunk(**item) for item in raw]
            self.embeddings = np.load(embeddings_file)

    @staticmethod
    def _chunk_text(text: str) -> list[str]:
        text = " ".join(text.split())
        if not text:
            return []

        chunks = []
        start = 0

        while start < len(text):
            end = min(start + CHUNK_SIZE, len(text))
            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            if end >= len(text):
                break

            start = max(end - CHUNK_OVERLAP, start + 1)

        return chunks

    def add_conversation(self, data: dict[str, Any]) -> dict[str, Any]:
        source = data.get("source", {})
        conversation = data.get("conversation", {})

        conversation_id = (
            source.get("captured_at")
            or source.get("url")
            or f"conversation-{len(self.chunks) + 1}"
        )

        platform = source.get("platform", "Unknown")
        new_chunks: list[Chunk] = []

        for message in conversation.get("messages", []):
            role = message.get("role", "unknown")
            content = message.get("content", "")
            message_id = int(message.get("id", 0))

            for part_no, chunk_text in enumerate(self._chunk_text(content)):
                new_chunks.append(
                    Chunk(
                        id=f"{conversation_id}-{message_id}-{part_no}",
                        text=chunk_text,
                        conversation_id=str(conversation_id),
                        platform=platform,
                        role=role,
                        message_ids=[message_id],
                    )
                )

        if not new_chunks:
            return {"chunks_added": 0}

        vectors = self.model.encode(
            [c.text for c in new_chunks],
            normalize_embeddings=True,
            convert_to_numpy=True,
        )

        self.chunks.extend(new_chunks)

        if self.embeddings is None:
            self.embeddings = vectors
        else:
            self.embeddings = np.vstack([self.embeddings, vectors])

        self._save_index()

        return {
            "chunks_added": len(new_chunks),
            "total_chunks": len(self.chunks),
            "platform": platform,
            "conversation_id": str(conversation_id),
        }

    def search(self, query: str, top_k: int = TOP_K) -> list[dict[str, Any]]:
        if not self.chunks or self.embeddings is None:
            return []

        query_vector = self.model.encode(
            [query],
            normalize_embeddings=True,
            convert_to_numpy=True,
        )[0]

        scores = self.embeddings @ query_vector
        top_indices = np.argsort(scores)[::-1][:top_k]

        results = []
        for index in top_indices:
            chunk = self.chunks[int(index)]
            results.append(
                {
                    "score": round(float(scores[index]), 4),
                    "text": chunk.text,
                    "platform": chunk.platform,
                    "role": chunk.role,
                    "conversation_id": chunk.conversation_id,
                    "message_ids": chunk.message_ids,
                }
            )

        return results

    def build_rag_context(self, query: str, top_k: int = TOP_K) -> str:
        results = self.search(query, top_k)

        if not results:
            return "No relevant conversation context was found."

        blocks = []
        for i, result in enumerate(results, start=1):
            blocks.append(
                f"[Context {i} | score={result['score']} | "
                f"{result['platform']} | {result['role']}]\n"
                f"{result['text']}"
            )

        return "\n\n".join(blocks)

    def _save_index(self):
        with (INDEX_DIR / "chunks.pkl").open("wb") as f:
            pickle.dump([asdict(c) for c in self.chunks], f)

        np.save(INDEX_DIR / "embeddings.npy", self.embeddings)
