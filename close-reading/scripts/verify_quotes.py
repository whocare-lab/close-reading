#!/usr/bin/env python3
"""Check that quotes in a reading card exist verbatim in the PDF, and on which PDF page.

Usage:
    python verify_quotes.py paper.pdf card.md

Reads every "double-quoted" English passage (8+ words) in the card, normalizes
whitespace, line-break hyphenation and typographic quotes on both sides, and
reports the PDF page(s) where each quote is found. Requires `pdftotext`
(poppler-utils).

Exit code 1 if any quote is not found.
"""
import re
import subprocess
import sys
import unicodedata


def page_texts(pdf):
    """Return per-page text with running headers/footers and bare page numbers removed,
    so quotes that cross a page break can still be matched."""
    out = subprocess.run(["pdftotext", pdf, "-"], capture_output=True, text=True, check=True).stdout
    pages = [p.splitlines() for p in out.split("\f")]

    def key(line):
        return re.sub(r"\d+", "#", line.strip().lower())

    counts = {}
    for lines in pages:
        for k in {key(l) for l in lines if l.strip()}:
            counts[k] = counts.get(k, 0) + 1
    repeated = {k for k, c in counts.items() if c >= 3 and len(k) < 120}
    cleaned = []
    for lines in pages:
        keep = [l for l in lines
                if l.strip() and key(l) not in repeated and not re.fullmatch(r"\s*\d{1,4}\s*", l)]
        cleaned.append("\n".join(keep))
    return cleaned


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("­", "")
    s = re.sub(r"[‘’‛′]", "'", s)
    s = re.sub(r"[“”‟″]", '"', s)
    s = re.sub(r"[‐‑‒–—―]", "-", s)
    s = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", s)  # rejoin words split across lines
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def quotes(card):
    text = open(card, encoding="utf-8").read()
    found = re.findall(r"[\"“]([^\"“”]{20,}?)[\"”]", text)
    return [q for q in found if len(q.split()) >= 8 and re.search(r"[A-Za-z]", q)]


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    pdf, card = sys.argv[1], sys.argv[2]
    pages = [norm(p) for p in page_texts(pdf)]
    joined = " ".join(pages)
    starts, pos = [], 0
    for p in pages:
        starts.append(pos)
        pos += len(p) + 1
    missing = 0
    for q in quotes(card):
        nq = norm(q).strip(' .,;:')
        idx = joined.find(nq)
        if idx < 0:
            missing += 1
            print(f"NOT FOUND : {q[:90]}")
            continue
        first = max(i for i, s in enumerate(starts) if s <= idx) + 1
        last = max(i for i, s in enumerate(starts) if s <= idx + len(nq) - 1) + 1
        span = f"PDF p.{first}" if first == last else f"PDF pp.{first}-{last}"
        print(f"OK {span:<12}: {q[:90]}")
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
