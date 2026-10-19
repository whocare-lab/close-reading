# close-reading | Close Reading and Literature Synthesis Skills for Qualitative Management Research

[繁體中文](README.md) ｜ **English**

Two Claude skills for graduate students in management doing qualitative and case-study research, from reading one paper to writing the literature review:

```
English paper (PDF) ──► close-reading (one paper) ──► reading card + literature matrix ──► lit-synthesis (many papers) ──► concept matrix, argument outline, research gaps, draft review
```

| Skill | Purpose | Trigger |
|---|---|---|
| **close-reading** | Close-read one English paper into a reading card you can always check against the original | Upload a PDF and say "close-read this paper" |
| **lit-synthesis** | Integrate several read papers into an argued literature review | "synthesize these papers", "write my literature review", "identify research gaps" |

The skills install separately; installing both is recommended, because lit-synthesis works best on close-reading's reading cards.

---

## Skill 1: close-reading

| Output | What it contains | Trigger |
|---|---|---|
| **A. Reading card** (always) | Core claim, research question, theoretical framework, method, findings, mechanism, contributions, limitations, **mind map**, **color-coded highlight list**, key quotes, relevance to your research, reviewer's view | "close-read this paper" |
| **B. Highlighted PDF** | Color highlights with pop-up notes on a copy of the PDF; the original is never modified | Automatic when Python can run |
| **C. Paragraph-by-paragraph bilingual text** | Each English paragraph followed by its Chinese translation, with a glossary | "make a bilingual version" |

Fixed highlight colors: 🟨 yellow = core concepts and claims | 🟩 green = method and design | 🟦 blue = evidence and findings | 🟥 red = limitations and open questions.

`verify_quotes.py` checks every quote, highlight and bilingual paragraph against the PDF, tolerating line breaks, hyphenation, drop caps, running headers and page-break interruptions, while flagging any word that was added, dropped or changed.

---

## Skill 2: lit-synthesis

| Output | What it contains |
|---|---|
| **A. Concept matrix** | Source list, coverage check (period, method, context, level of analysis, theory, strength of evidence), papers × concepts matrix with page numbers, patterns |
| **B. Argument outline** | Funnel-shaped section structure: one claim per section, topic sentence and sources per paragraph, transitions; Mermaid literature map and suggested reading list |
| **C. Research gap statement** | Each gap typed (confusion, neglect, application, problematization), backed by matrix evidence, stating what is missing, why it matters and how your study addresses it |
| **D. Draft review** (on request) | Concept-centric academic paragraphs with APA 7th citations and a reference list |

How it differs from "ask an AI to write my literature review":
- **Concept-centric, not author-by-author.**
- **Every synthesized claim has at least two sources**, or is labeled single-source; disagreements must be explained.
- **Only the papers you supplied are cited**; anything else goes to "suggested reading", never into the text.
- **No empty gap statements** such as "little research has examined…" without evidence.
- **Warns when the corpus is thin**: under 5 papers is labeled preliminary; under 3, no definitive gaps.
- **`check_citations.py`** checks in-text citations against the reference list, flags cited works without a reading card (possibly added from memory), and checks APA 7 "et al." usage. Handles English and Chinese citations.

---

## Installation

1. Fill in `close-reading/references/my-research.md` and copy it to `lit-synthesis/references/my-research.md`. lit-synthesis needs your research question to judge gaps; without it, it asks you first.
2. **claude.ai**: upload `dist/close-reading.zip` and `dist/lit-synthesis.zip` in the Skills section of settings (re-zip the folders if you edited `my-research.md`).
3. **Claude Code**:
```bash
git clone https://github.com/whocare-lab/close-reading.git
cp -R close-reading/close-reading close-reading/lit-synthesis ~/.claude/skills/
pip install pypdf pypdfium2
```

## Examples and tests

- **close-reading** was tested on Adner (2017), a peer-reviewed conceptual article, and Pidun, Reeves, & Knust (2021), a BCG report: all card quotes, PDF highlights and 159 bilingual paragraphs passed the verbatim check, and the checker caught all nine kinds of deliberate tampering.
- **lit-synthesis** was tested by synthesizing those two reading cards (`examples/synthesis/`): it raised the thin-corpus warning, found zero empirical studies and no non-profit or education context, identified one disagreement and one shared assumption, and its draft passed both the citation check and the quote check across both PDFs. Two papers are only a demonstration.

Full bilingual texts and highlighted PDFs reproduce the originals and are not published here for copyright reasons.

## Notes
- Reading cards, translations and draft reviews are study aids, **not citable or submittable work**. Cite the English original and rewrite drafts in your own words.
- "No study has examined…" is a strong claim; the skill can only judge from the papers you supplied.

## Acknowledgments and license
close-reading's bilingual reading, color highlights and mind maps are inspired by [YuriyLin/PaperRead](https://github.com/YuriyLin/PaperRead) (MIT); no code from it is used. Method references for lit-synthesis are in `lit-synthesis/references/synthesis-methods.md`. MIT License.
