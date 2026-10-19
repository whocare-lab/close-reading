#!/usr/bin/env python3
"""Check APA 7th citation consistency in a literature review draft or outline.

Usage:
    python check_citations.py draft.md [matrix.csv]

Reports:
  1. Cited in text but missing from the reference list
  2. In the reference list but never cited
  3. Cited but not in the literature matrix (no reading card: possibly added
     from memory; verify before use)            -- only when matrix.csv is given
  4. Same source written in different forms, and 3+ author citations not
     shortened to "et al." (APA 7th rule)

Understands English and Chinese citations, e.g.
  (Adner, 2017, p. 42)  (Adner, 2017; Pidun et al., 2021)  Adner (2017)
  Sandberg and Alvesson (2011)  （張三，2020）  張三與李四（2020）  張三等人（2020）

The reference list is everything after a heading containing "參考文獻" or
"References". A section headed "建議補讀" or "Further reading" is skipped. Exit code 1 if problem 1 or 3 is found.
"""
import csv
import re
import sys
from collections import defaultdict

YEAR = r"(?:\d{4}[a-z]?|n\.d\.|in press|印行中)"
CJK = "一-鿿"
PREFIX = re.compile(r"^(?:e\.g\.,?|see also|see|cf\.|i\.e\.,?|例如|參見|見|如)\s*", re.I)
SPLIT_AUTH = re.compile(r"\s*(?:,|，|、|&|\band\b|與|和|及|et al\.|等人|等)\s*")


def first_author(authors):
    a = PREFIX.sub("", authors.strip())
    parts = [p for p in SPLIT_AUTH.split(a) if p.strip()]
    return parts[0].strip().lower() if parts else a.lower()


def n_listed(authors):
    if re.search(r"et al\.|等人|等$", authors):
        return 99  # shortened form
    return len([p for p in re.split(r"\s*(?:,|，|、|&|\band\b|與|和|及)\s*", authors) if p.strip()])


def split_doc(text):
    m = re.search(r"^#{1,6}\s*.*(參考文獻|References).*$", text, re.M | re.I)
    if not m:
        m = re.search(r"^\s*(參考文獻|References)\s*$", text, re.M | re.I)
    return (text[:m.start()], text[m.end():]) if m else (text, "")


def in_text_citations(body):
    found = []  # (key, form, kind)
    # parenthetical: (... 2017 ...) or full-width parentheses
    for grp in re.findall(r"[（(]([^()（）]*?\d{4}[a-z]?[^()（）]*)[)）]", body):
        for part in re.split(r"[;；]", grp):
            part = PREFIX.sub("", part.strip())
            m = re.match(rf"^(?P<a>.+?)[,，]\s*(?P<y>{YEAR})(?:\s*[,，].*)?$", part)
            if m and re.search(rf"[A-Za-z{CJK}]", m.group("a")) and not re.match(r"^(p|pp)\.", m.group("a")):
                found.append(((first_author(m.group("a")), m.group("y")), m.group("a").strip(), "paren"))
    # narrative, English: Adner (2017), Pidun et al. (2021), Sandberg and Alvesson (2011)
    name = r"(?:[A-Z][a-z]+\s)?[A-Z][A-Za-z'’\-]+"
    for m in re.finditer(
            rf"(?P<a>{name}(?:\s?(?:et al\.|等人)|\s?(?:&|and|與|和)\s?{name}|(?:,\s{name})+,?\s(?:&|and)\s{name})?)\s?[（(](?P<y>{YEAR})(?:[,，][^)）]*)?[)）]",
            body):
        found.append(((first_author(m.group("a")), m.group("y")), m.group("a").strip(), "narrative"))
    # narrative, Chinese: 張三（2020） 張三與李四（2020） 張三等人（2020）
    for m in re.finditer(
            rf"(?P<a>[{CJK}]{{2,4}}(?:等人|(?:與|和|、)[{CJK}]{{2,4}})?)[（(](?P<y>\d{{4}}[a-z]?)(?:[,，][^)）]*)?[)）]",
            body):
        found.append(((first_author(m.group("a")), m.group("y")), m.group("a").strip(), "narrative-zh"))
    return found


def reference_keys(refs):
    keys = {}
    for line in refs.splitlines():
        line = re.sub(r"^\s*(?:[-*+]|\d+\.)\s+", "", line).strip()
        if not line:
            continue
        m = re.search(rf"[（(](?P<y>{YEAR})(?:,[^)）]*)?[)）]", line)
        if not m:
            continue
        authors = line[:m.start()]
        keys[(first_author(authors), m.group("y"))] = line[:90]
    return keys


def matrix_keys(path):
    keys = set()
    with open(path, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            short, year = row.get("apa_short", ""), row.get("year", "")
            m = re.search(rf"({YEAR})", short)
            y = m.group(1) if m else year.strip()
            keys.add((first_author(re.sub(rf"[,，]?\s*{YEAR}.*$", "", short)), y))
    return keys


def main():
    if len(sys.argv) not in (2, 3):
        print(__doc__)
        sys.exit(2)
    text = open(sys.argv[1], encoding="utf-8").read()
    body, refs = split_doc(text)
    # a suggested-reading section lists works not yet read on purpose: skip it
    body = re.split(r"^#{1,6}\s*.*(建議補讀|延伸閱讀|Further reading|Suggested reading).*$",
                    body, maxsplit=1, flags=re.M | re.I)[0]
    cites = in_text_citations(body)
    refkeys = reference_keys(refs)
    mkeys = matrix_keys(sys.argv[2]) if len(sys.argv) == 3 else None

    cited = defaultdict(set)
    for key, form, kind in cites:
        cited[key].add(form)

    def label(k):
        return f"{k[0].title()}, {k[1]}"

    problems = 0
    print(f"文內引用：{len(cites)} 次，{len(cited)} 篇不同文獻；參考文獻清單：{len(refkeys)} 筆")

    if refs:
        miss = sorted(k for k in cited if k not in refkeys)
        print("\n[1] 文內有引用、參考文獻清單沒有：" + ("無" if not miss else ""))
        for k in miss:
            print(f"    - {label(k)}　寫法：{' / '.join(sorted(cited[k]))}")
        problems += len(miss)
        unused = sorted(k for k in refkeys if k not in cited)
        print("\n[2] 參考文獻清單有、文內沒引用：" + ("無" if not unused else ""))
        for k in unused:
            print(f"    - {refkeys[k]}")
    else:
        print("\n[1][2] 找不到「參考文獻」或「References」標題，略過清單比對（大綱可忽略）")

    if mkeys is not None:
        nomat = sorted(k for k in cited if k not in mkeys)
        print("\n[3] 有引用、但不在文獻矩陣（沒有精讀卡，請確認不是憑記憶加入）：" + ("無" if not nomat else ""))
        for k in nomat:
            print(f"    - {label(k)}")
        problems += len(nomat)

    print("\n[4] 寫法不一致或未依 APA 7 縮寫：", end="")
    notes = []
    for k, forms in sorted(cited.items()):
        shortened = {f for f in forms if re.search(r"et al\.|等人", f)}
        if shortened and len(forms - shortened) and any(n_listed(f) >= 2 for f in forms - shortened):
            notes.append(f"    - {label(k)}：同時出現 {' / '.join(sorted(forms))}")
        for f in forms:
            if 3 <= n_listed(f) < 99:
                notes.append(f"    - {label(k)}：「{f}」三位以上作者應寫成「第一作者 et al.」或「第一作者等人」")
    print("無" if not notes else "")
    for n in sorted(set(notes)):
        print(n)

    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
