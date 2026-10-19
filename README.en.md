# close-reading | Close Reading of English Papers for Qualitative Management Research

[繁體中文](README.md) ｜ **English**

A Claude skill for graduate students in management doing qualitative and case-study research.
Upload an English paper as a PDF and say "close-read this paper". Claude produces reading material you can always check back against the original.

> **Next step: multi-paper synthesis.** After reading several papers, use the `lit-synthesis` skill in [whocare-lab/overview-reading](https://github.com/whocare-lab/overview-reading) to turn the reading cards and `matrix.csv` into a concept matrix, argument outline, research gaps and a draft literature review.

## Three outputs

| Output | What it contains | How to trigger |
|---|---|---|
| **A. Reading card** (always) | Core claim, research question, theoretical framework, method, findings, mechanism, contributions, limitations, **mind map**, **color-coded highlight list**, key quotes, relevance to your own research, reviewer's view | "close-read this paper" |
| **B. Highlighted PDF** | Color highlights drawn on a copy of the PDF, each with a pop-up note; the original file is never modified | Produced automatically when Python can run |
| **C. Paragraph-by-paragraph bilingual text** | Each English paragraph followed by its Chinese translation, with a glossary and section/page markers | "make a bilingual version", "translate paragraph by paragraph" |

### Fixed highlight colors

| Color | Meaning |
|---|---|
| 🟨 Yellow | Core concepts and main claims |
| 🟩 Green | Method, research design, analytical framework |
| 🟦 Blue | Evidence, data, findings and numbers |
| 🟥 Red | Limitations, boundary conditions, open questions |

### Mind map
Written in Mermaid, which renders directly on GitHub, Obsidian, Typora and claude.ai. First-level branches are always: research question, theoretical framework, method, findings, contributions, limitations.

## Output language

Traditional Chinese by default. Ask in English, or say "English", and the reading card is written in English. The bilingual output (C) remains English original plus Chinese translation unless you ask for another target language.

## Quality checks

- **Verbatim quote check**: `scripts/verify_quotes.py` compares every quote and highlight in a reading card, and every English paragraph in a bilingual file, against the PDF. It ignores line breaks, hyphenation, drop caps and running headers, and accepts paragraphs interrupted by a footnote or table across a page break, but flags any word that was added, dropped or changed.
- Quotes carry printed page numbers; the offset between PDF page order and printed pages is computed.
- Missing bibliographic fields are marked "to verify" rather than filled from memory; draft, preprint and internal versions trigger a version warning.
- Evaluation criteria follow the article type: qualitative empirical, quantitative empirical, conceptual, review, or practitioner article.
- Content is tagged as author's claim, evidence, or the reader's interpretation.

## Installation

### 1. Describe your research
Fill in `close-reading/references/my-research.md` (title, research questions, data, theoretical lenses, actual chapter headings). The skill works without it, but then it cannot map a paper to your own chapters.

### 2a. claude.ai (web, desktop, mobile)
1. Download `dist/close-reading.zip`. If you edited `my-research.md`, re-zip the `close-reading` folder.
2. Upload the zip in the Skills section of claude.ai settings.
3. In a new chat, upload a PDF and say "close-read this paper".

### 2b. Claude Code
```bash
git clone https://github.com/whocare-lab/close-reading.git
cp -R close-reading/close-reading ~/.claude/skills/        # macOS / Linux
# Windows (PowerShell):
# Copy-Item -Recurse close-reading\close-reading $env:USERPROFILE\.claude\skills\
pip install pypdf pypdfium2
```
Outputs go to `literature/` in the current project (`cards/`, `annotated/`, `bilingual/`), and a row is appended to `literature/matrix.csv`.

## Examples and tests

Tested on two very different documents (with an empty `my-research.md`):

| Document | Type | Result |
|---|---|---|
| Adner (2017), *Journal of Management* | Peer-reviewed conceptual article | Correctly resolved online-first 2016 vs. issue year 2017 and a PDF-to-journal page offset of 38; 22 card quotes and highlights, 17 PDF highlights and all 95 English paragraphs of the full bilingual text passed the verbatim check |
| Pidun, Reeves, & Knust (2021), BCG | Consulting report | Classified as a practitioner article, not empirical evidence; detected the "EARLY DRAFT—INTERNAL BCG USE ONLY" banner on pp. 6–11 and issued a version warning; 16 card quotes, 11 PDF highlights and all 64 bilingual paragraphs passed |

The checker was also tested against nine kinds of tampering (one changed word, a changed number, a dropped clause, words added at the end, and so on); all were caught.

`examples/` contains only reading cards and the literature matrix. **Full bilingual texts and highlighted PDFs reproduce the original and are not published here for copyright reasons**; generate them from PDFs you have legitimate access to, for personal reading only.

## Notes

- Reading cards and translations are study aids, **not citable sources**. Cite the English original with page numbers.
- Scanned PDFs or PDFs with garbled text layers reduce quote accuracy; the skill then paraphrases and flags it.
- Do not put unpublished interview data or participant information in `my-research.md` if you share your copy.

## Acknowledgments and license

The ideas of paragraph-by-paragraph bilingual reading, fixed-meaning color highlights and paper mind maps come from [YuriyLin/PaperRead](https://github.com/YuriyLin/PaperRead) (MIT License). No code from that project is used; this is an independent re-implementation as a Claude skill, adapted for qualitative management research.

MIT License.
