import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.rag.chunking import split_text


def test_short_text_single_chunk():
    text = "This is a short policy note."
    chunks = split_text(text, chunk_size=800, overlap=120)
    assert len(chunks) == 1
    assert "short policy note" in chunks[0]


def test_long_text_produces_multiple_chunks():
    paragraph = "Ceylon cinnamon is graded by quill diameter. " * 60
    text = paragraph + "\n\n" + paragraph
    chunks = split_text(text, chunk_size=800, overlap=120)
    assert len(chunks) > 1


def test_paragraphs_are_not_split_when_they_fit():
    p1 = "Paragraph one about shipping terms."
    p2 = "Paragraph two about payment terms."
    text = f"{p1}\n\n{p2}"
    chunks = split_text(text, chunk_size=800, overlap=120)
    assert len(chunks) == 1
    assert p1 in chunks[0] and p2 in chunks[0]


def test_overlap_present_between_consecutive_chunks():
    paragraph = "Reorder point analysis for cardamom stock levels. " * 40
    text = paragraph + "\n\n" + paragraph + "\n\n" + paragraph
    chunks = split_text(text, chunk_size=300, overlap=60)
    assert len(chunks) >= 2
    # second chunk should start with the tail of the first (the overlap)
    tail_of_first = chunks[0][-60:]
    assert tail_of_first[:20] in chunks[1]
