#!/usr/bin/env python3
"""Check that English text in a reading card or bilingual file exists verbatim in the PDF.

Usage:
    python verify_quotes.py paper.pdf card_or_bilingual.md
    python verify_quotes.py a.pdf b.pdf c.pdf review_draft.md   (several papers)

Checks two kinds of English text (8+ words) against the PDF:
  - every "double-quoted" passage in a reading card, and
  - every English paragraph written as a "> " blockquote in a bilingual file.

Matching ignores whitespace, hyphens/dashes, ligatures, typographic quotes,
running headers/footers and bare page numbers, so line breaks, drop caps and
words split across lines do not cause false alarms. A passage interrupted by a
footnote, table or page break is accepted only when the interruption crosses a
page boundary; any word dropped, added or changed inside a page is reported.

Text is extracted with pdftotext (poppler) and, if installed, pypdfium2; a passage
passes if it matches either extraction (two-column pages are sometimes read in a
different order by one of them). Reports the PDF page(s) of each match.
Exit code 1 if any passage is not found.
"""
import os
import re
import subprocess
import sys
import unicodedata


def _clean(pages):
    """Drop running headers/footers (lines repeated on 3+ pages) and bare page numbers."""
    pages = [p.splitlines() for p in pages]

    def key(line):
        return re.sub(r"\d+", "#", line.strip().lower())

    def edges(lines):  # only the first/last few lines of a page can be headers or footers
        body = [i for i, l in enumerate(lines) if l.strip()]
        return set(body[:3] + body[-3:])

    counts = {}
    for lines in pages:
        for k in {key(lines[i]) for i in edges(lines)}:
            counts[k] = counts.get(k, 0) + 1
    repeated = {k for k, c in counts.items() if c >= 3 and len(k) < 120}
    cleaned = []
    for lines in pages:
        e = edges(lines)
        cleaned.append("\n".join(
            l for i, l in enumerate(lines)
            if l.strip() and not (i in e and (key(l) in repeated or re.fullmatch(r"\s*\d{1,4}\s*", l)))))
    return cleaned


def extractions(pdf):
    out = []
    try:
        txt = subprocess.run(["pdftotext", pdf, "-"], capture_output=True, text=True, check=True).stdout
        out.append(("pdftotext", _clean(txt.split("\f"))))
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass
    try:
        import pypdfium2 as pdfium
        doc = pdfium.PdfDocument(pdf)
        pages = []
        for page in doc:
            tp = page.get_textpage()
            pages.append(tp.get_text_range(0, tp.count_chars()).replace("\r\n", "\n"))
        out.append(("pdfium", _clean(pages)))
    except Exception:
        pass
    if not out:
        sys.exit("Cannot extract text: install poppler-utils (pdftotext) or `pip install pypdfium2`.")
    return out


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = re.sub("[­￾\x02]", "", s)  # soft hyphens / extractor hyphen markers
    s = re.sub("[‘’‛′`]", "'", s)
    s = re.sub("[“”‟″]", '"', s)
    s = re.sub("[-‐-―−]", "", s)  # hyphens/dashes are ambiguous at line ends
    s = re.sub(r"\s+", "", s)  # spacing differs between extractors (drop caps, line joins)
    return s.lower()


def quotes(path):
    lines = open(path, encoding="utf-8").read().splitlines()
    text = "\n".join(l for l in lines if not l.startswith(">"))  # blockquotes are checked whole
    found = re.findall("[\"“]([^\"“”\\n]{20,}?)[\"”]", text)
    cjk = "[　-〿一-鿿＀-￯]"  # text between two separate quotes
    return [q for q in found if len(q.split()) >= 8 and re.search("[A-Za-z]", q)
            and not re.search(cjk, q)]


def blocks(path):
    """English paragraphs written as '> ' blockquotes (bilingual files)."""
    paras, cur = [], []
    for line in open(path, encoding="utf-8"):
        if line.startswith(">"):
            cur.append(line[1:].strip())
        elif cur:
            paras.append(" ".join(cur))
            cur = []
    if cur:
        paras.append(" ".join(cur))
    # list markers ("1.", "(a)", bullets) are often not in the PDF text layer
    paras = [re.sub("^\\s*(?:\\d{1,2}[.)]|\\([a-z0-9]{1,3}\\)|[•▪◦*-])\\s+", "", p)
             for p in paras]
    return [p for p in paras if len(p.split()) >= 8 and re.search("[A-Za-z]{3}", p)
            and not re.search("[一-鿿]", p)]


def segmented(hay, needle, page_of, min_chars=20, max_gap=6000, max_breaks=4):
    """Ordered match of needle as a few long segments. A skip between segments is
    accepted only if it crosses a page boundary. Returns segment offsets or None."""
    pos, i, hits = 0, 0, []
    while i < len(needle):
        rest = len(needle) - i
        if hits and rest < min_chars:  # a short dangling tail is not trustworthy
            return None
        lo, hi, best = min(min_chars, rest), rest, None
        while lo <= hi:  # longest prefix of the remaining text that can be placed
            mid = (lo + hi) // 2
            k = hay.find(needle[i:i + mid], pos)
            ok = k >= 0 and (not hits or k == pos or
                             (k - pos <= max_gap and page_of(k) != page_of(pos - 1)))
            if ok:
                best, lo = (mid, k), mid + 1
            else:
                hi = mid - 1
        if not best or len(hits) > max_breaks:
            return None
        n, k = best
        hits.append(k)
        pos, i = k + n, i + n
    return hits


def locate(hay, starts, needle):
    page_of = lambda x: max(p for p, s in enumerate(starts) if s <= x) + 1
    k = hay.find(needle)
    if k >= 0:
        return page_of(k), page_of(k + len(needle) - 1), 0
    hits = segmented(hay, needle, page_of)
    if hits:
        return page_of(hits[0]), page_of(hits[-1]), len(hits) - 1
    return None


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    pdfs, path = sys.argv[1:-1], sys.argv[-1]
    hays = []  # (pdf name, joined text, page starts)
    for pdf in pdfs:
        for name, pages in extractions(pdf):
            normed = [norm(p) for p in pages]
            starts, pos = [], 0
            for p in normed:
                starts.append(pos)
                pos += len(p)
            hays.append((pdf, "".join(normed), starts))
    many = len(pdfs) > 1
    missing = 0
    for q in quotes(path) + blocks(path):
        nq = norm(q).strip('.,;:')
        res = next(((pdf, r) for pdf, h, s in hays for r in [locate(h, s, nq)] if r), None)
        if not res:
            missing += 1
            print(f"NOT FOUND : {q[:90]}")
            continue
        pdf, (first, last, breaks) = res
        span = f"PDF p.{first}" if first == last else f"PDF pp.{first}-{last}"
        if many:
            span = f"{os.path.basename(pdf)} {span}"
        note = f" (across {breaks} page-break interruption(s))" if breaks else ""
        print(f"OK {span:<12}: {q[:90]}{note}")
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
