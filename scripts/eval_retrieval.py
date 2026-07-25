"""
Retrieval evaluation script (required deliverable, section 4d).

Run this after `pip install -r requirements.txt` in an environment with
internet access (the sentence-transformers model is downloaded on first
run). It runs 5 representative queries against the real embedding-based
RAGPipeline and prints the top retrieved chunks with their source files
and similarity scores, so you can eyeball whether retrieval is relevant.

Usage:
    python scripts/eval_retrieval.py

Paste the output (or a summary + your commentary) into the
"Retrieval Evaluation" section of README.md before submission.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.rag.pipeline import RAGPipeline  # noqa: E402

SAMPLE_QUERIES = [
    "What is the minimum order quantity for cardamom?",
    "Do you offer Halal or Kosher certification?",
    "What are the payment terms for a new buyer?",
    "How long does shipping take to the EU?",
    "What happens if I receive damaged goods and want a refund?",
]


def main() -> None:
    kb_dir = os.path.join(os.path.dirname(__file__), "..", "data", "knowledge_base")
    rag = RAGPipeline(kb_dir=kb_dir)
    print("Building/loading index...")
    rag.ensure_ready()
    print(f"Indexed {len(rag.chunks)} chunks from the knowledge base.\n")

    for q in SAMPLE_QUERIES:
        print("=" * 80)
        print(f"QUERY: {q}")
        results = rag.retrieve(q, k=3)
        for i, r in enumerate(results, start=1):
            print(f"\n  [{i}] source={r.chunk.source}  score={r.score:.3f}")
            snippet = r.chunk.text.replace("\n", " ")[:220]
            print(f"      {snippet}...")
        print()


if __name__ == "__main__":
    main()
