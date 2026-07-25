"""
Text chunking logic, deliberately kept free of heavy dependencies
(no faiss / sentence-transformers imports here) so it can be unit
tested quickly and in isolation from the embedding/index layer.
"""

from __future__ import annotations

import re
from typing import List

CHUNK_SIZE = 800
CHUNK_OVERLAP = 120


def split_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Paragraph-aware recursive splitter with fallback to hard character
    windows for oversized paragraphs, plus a sliding overlap between
    consecutive chunks for retrieval continuity."""
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks: List[str] = []
    buf = ""
    for para in paragraphs:
        if len(buf) + len(para) + 1 <= chunk_size:
            buf = f"{buf}\n{para}" if buf else para
        else:
            if buf:
                chunks.append(buf)
            if len(para) <= chunk_size:
                buf = para
            else:
                start = 0
                while start < len(para):
                    end = start + chunk_size
                    chunks.append(para[start:end])
                    start = end - overlap
                buf = ""
    if buf:
        chunks.append(buf)

    overlapped = []
    for i, c in enumerate(chunks):
        if i == 0:
            overlapped.append(c)
        else:
            prev_tail = chunks[i - 1][-overlap:]
            overlapped.append(prev_tail + "\n" + c)
    return overlapped or [text]
