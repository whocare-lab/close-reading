#!/usr/bin/env python3
"""Add color-coded highlights with notes to a copy of a PDF.

Usage:
    python annotate_pdf.py paper.pdf annotations.json output.pdf

annotations.json is a list of objects:
    {"text": "exact English passage from the PDF",
     "type": "claim" | "method" | "evidence" | "limit",
     "note": "中文註記（會顯示在標註的彈出說明）",
     "page": 5}            # optional: PDF page number (1-based) to search first

Fixed color meaning (same for every paper):
    claim    yellow  核心概念與主要主張
    method   green   方法與研究設計
    evidence blue    證據、資料與研究發現
    limit    red     限制、邊界條件與待研究問題

The original PDF is never modified. Passages that cannot be located are listed
and skipped, never guessed. Requires: pip install pypdf pypdfium2
"""
import json
import re
import sys
import unicodedata

try:
    import pypdfium2 as pdfium
    from pypdf import PdfReader, PdfWriter
    from pypdf.annotations import Highlight
    from pypdf.generic import ArrayObject, FloatObject, NameObject, TextStringObject
except ImportError:
    print("Missing packages. Run: pip install pypdf pypdfium2")
    sys.exit(2)

COLORS = {
    "claim": ("fff176", "核心主張"),
    "method": ("a5d6a7", "方法"),
    "evidence": ("90caf9", "證據"),
    "limit": ("ef9a9a", "限制"),
}


def normalize_with_map(raw):
    """Normalize text for matching; return (normalized, index map into raw)."""
    out, idx = [], []
    i, n = 0, len(raw)
    while i < n:
        ch = unicodedata.normalize("NFKC", raw[i])
        if ch in "­￾\x02":  # soft hyphen / pdfium hyphen markers
            i += 1
            continue
        # Hyphens and dashes are ambiguous at line ends ("co-\ninnovation" vs
        # "inter-\ndependence"), so drop them, and any spaces around them, on both sides.
        if ch in "-‐‑‒–—―":
            while out and out[-1] == " ":
                out.pop()
                idx.pop()
            j = i + 1
            while j < n and raw[j].isspace():
                j += 1
            i = j
            continue
        if ch in "‘’‛′":
            ch = "'"
        elif ch in "“”‟″":
            ch = '"'
        if ch.isspace():
            if out and out[-1] == " ":
                i += 1
                continue
            ch = " "
        for c in ch.lower():
            out.append(c)
            idx.append(i)
        i += 1
    return "".join(out), idx


def norm_query(s):
    s, _ = normalize_with_map(s)
    return s.strip(" .,;:")


def find_rects(doc, query, page_hint=None):
    """Return (page_index, [rects]) for the first match, preferring page_hint."""
    order = list(range(len(doc)))
    if page_hint and 1 <= page_hint <= len(doc):
        order.remove(page_hint - 1)
        order.insert(0, page_hint - 1)
    q = norm_query(query)
    for pi in order:
        tp = doc[pi].get_textpage()
        raw = tp.get_text_range(0, tp.count_chars())
        norm, imap = normalize_with_map(raw)
        k = norm.find(q)
        if k < 0:
            continue
        start, end = imap[k], imap[k + len(q) - 1]
        count = end - start + 1
        rects = [tp.get_rect(r) for r in range(tp.count_rects(start, count))]
        return pi, [r for r in rects if r[2] - r[0] > 1]
    return None, []


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(2)
    src, ann_path, dst = sys.argv[1:]
    items = json.load(open(ann_path, encoding="utf-8"))
    doc = pdfium.PdfDocument(src)
    writer = PdfWriter(clone_from=PdfReader(src))
    missing = 0
    for it in items:
        kind = it.get("type", "claim")
        color, label = COLORS.get(kind, COLORS["claim"])
        pi, rects = find_rects(doc, it["text"], it.get("page"))
        if pi is None or not rects:
            missing += 1
            print(f"NOT FOUND  [{label}] {it['text'][:80]}")
            continue
        quads = []
        for (l, b, r, t) in rects:
            quads += [l, t, r, t, l, b, r, b]
        bbox = (min(r[0] for r in rects), min(r[1] for r in rects),
                max(r[2] for r in rects), max(r[3] for r in rects))
        annot = Highlight(rect=bbox, quad_points=ArrayObject([FloatObject(v) for v in quads]),
                          highlight_color=color)
        annot[NameObject("/Contents")] = TextStringObject(f"【{label}】{it.get('note', '')}")
        annot[NameObject("/T")] = TextStringObject("close-reading")
        writer.add_annotation(page_number=pi, annotation=annot)
        print(f"OK p.{pi + 1:<4} [{label}] {it['text'][:70]}")
    with open(dst, "wb") as f:
        writer.write(f)
    print(f"\nSaved: {dst}  ({len(items) - missing} highlighted, {missing} not found)")
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
