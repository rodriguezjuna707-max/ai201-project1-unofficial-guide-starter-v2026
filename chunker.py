"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split on paragraph breaks, carrying the title line into every chunk.

    Written for campus_life, where `app.py index` showed the starter cutting
    nothing at all: the longest document is 549 characters against an 800
    character window, so 88 documents came out as 88 chunks. Several of those
    documents hold three or four separate topics, so one file is not one
    thought here.

    Three rules, in the order they apply:

      1. Split on blank lines. These documents already mark their own topic
         boundaries that way, and a character count would ignore them.
      2. One paragraph per chunk. Merge forward ONLY while a piece is still
         under MIN_CHARS, so headings and one line asides get absorbed but two
         paragraphs on different topics never get glued together just because
         there happened to be room for them.
      3. Prepend the title line to every chunk after the first. Each document
         names its subject once, in the title, so without this the paragraph
         about uneven heating doesn't say which building it belongs to.

    Rule 3 is what replaces the starter's 120 character overlap. See the
    Chunking Strategy section of the README for why.

    CHUNK_SIZE is a ceiling I check rather than a window I cut on: the longest
    paragraph in this corpus is 373 characters and the longest title is 47, so
    at 450 nothing is ever forced apart. If a future document does exceed it,
    the paragraph is kept whole and reported by `describe` as the longest
    chunk, because splitting mid sentence is the failure this chunker exists to
    avoid.
    """
    min_chars = config.CHUNK_MIN

    chunks: list[Chunk] = []
    for doc in documents:
        paragraphs = [p.strip() for p in doc.text.split("\n\n") if p.strip()]
        if not paragraphs:
            continue

        # The first line is the document's title. Everything after it is body.
        title = paragraphs[0].splitlines()[0].strip()
        body = paragraphs[1:] if len(paragraphs) > 1 else paragraphs

        # Rules 1 and 2: one paragraph per piece, absorbing anything too thin.
        pieces: list[str] = []
        for para in body:
            if pieces and len(pieces[-1]) < min_chars:
                pieces[-1] = f"{pieces[-1]}\n\n{para}"
            else:
                pieces.append(para)

        # A trailing piece below the floor has nothing after it to merge into,
        # so fold it backwards instead of storing a fragment.
        if len(pieces) > 1 and len(pieces[-1]) < min_chars:
            tail = pieces.pop()
            pieces[-1] = f"{pieces[-1]}\n\n{tail}"

        # Rule 3: every chunk carries the subject.
        for index, piece in enumerate(pieces):
            text = piece if piece.startswith(title) else f"{title}\n\n{piece}"
            chunks.append(
                Chunk(
                    text=text,
                    source=doc.source,
                    index=index,
                    produced_by="chunker.py::split_documents",
                )
            )

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
