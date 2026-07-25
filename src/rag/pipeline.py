"""
RAG Pipeline for Serendib Spice & Tea Traders Co-Pilot.

Design decisions (documented here and in README.md):
- Embedding model: sentence-transformers/all-MiniLM-L6-v2
    * Runs locally (no API cost/latency for embedding), 384-dim, well-suited
      for short domain documents like ours, and small enough to run
      comfortably on Streamlit Community Cloud's free tier.
- Vector store: FAISS (in-memory, persisted to disk as a flat index file)
    * Avoids SQLite version conflicts that Chroma sometimes hits on
      Streamlit Cloud, and is fast enough at our corpus scale (tens of
      documents / a few hundred chunks) without needing a hosted service.
- Chunking: recursive character splitting, ~800 chars with 120 char overlap,
  splitting preferentially at paragraph/sentence boundaries so a chunk
  doesn't cut a policy clause in half.
"""

from __future__ import annotations

import os
import pickle
from dataclasses import dataclass, field
from typing import List

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

from src.rag.chunking import split_text

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
INDEX_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "index")


@dataclass
class Chunk:
    text: str
    source: str
    chunk_id: int


@dataclass
class RetrievedChunk:
    chunk: Chunk
    score: float


class RAGPipeline:
    def __init__(self, kb_dir: str, index_dir: str = INDEX_DIR):
        self.kb_dir = kb_dir
        self.index_dir = index_dir
        self._model: SentenceTransformer | None = None
        self.chunks: List[Chunk] = []
        self.index: faiss.Index | None = None

    @property
    def model(self) -> SentenceTransformer:
        if self._model is None:
            self._model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        return self._model

    def build(self) -> None:
        """Ingest all documents in kb_dir, chunk them, embed, and build a
        FAISS index. Persists the index + chunk metadata to disk so it does
        not need to be rebuilt on every app restart."""
        self.chunks = []
        cid = 0
        for fname in sorted(os.listdir(self.kb_dir)):
            if not fname.endswith(".md"):
                continue
            path = os.path.join(self.kb_dir, fname)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            for piece in split_text(text):
                self.chunks.append(Chunk(text=piece, source=fname, chunk_id=cid))
                cid += 1

        texts = [c.text for c in self.chunks]
        embeddings = self.model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
        embeddings = np.asarray(embeddings, dtype="float32")

        dim = embeddings.shape[1]
        index = faiss.IndexFlatIP(dim)  # cosine sim via normalized vectors + inner product
        index.add(embeddings)
        self.index = index

        os.makedirs(self.index_dir, exist_ok=True)
        faiss.write_index(index, os.path.join(self.index_dir, "kb.index"))
        with open(os.path.join(self.index_dir, "chunks.pkl"), "wb") as f:
            pickle.dump(self.chunks, f)

    def load(self) -> bool:
        """Load a previously built index from disk. Returns False if not found."""
        idx_path = os.path.join(self.index_dir, "kb.index")
        chunks_path = os.path.join(self.index_dir, "chunks.pkl")
        if not (os.path.exists(idx_path) and os.path.exists(chunks_path)):
            return False
        self.index = faiss.read_index(idx_path)
        with open(chunks_path, "rb") as f:
            self.chunks = pickle.load(f)
        return True

    def ensure_ready(self) -> None:
        if not self.load():
            self.build()

    def retrieve(self, query: str, k: int = 5) -> List[RetrievedChunk]:
        if self.index is None:
            self.ensure_ready()
        q_emb = self.model.encode([query], normalize_embeddings=True)
        q_emb = np.asarray(q_emb, dtype="float32")
        scores, ids = self.index.search(q_emb, k)
        results = []
        for score, idx in zip(scores[0], ids[0]):
            if idx == -1:
                continue
            results.append(RetrievedChunk(chunk=self.chunks[idx], score=float(score)))
        return results
