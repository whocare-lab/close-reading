# close-reading-claude｜管理學質性研究英文文獻精讀 Skill

給管理學院做質性研究、個案研究的同學使用的 Claude skill。
上傳一篇英文文獻 PDF，說「精讀這篇」，Claude 會產出一張可以回原文核對的精讀卡。

## 它會做什麼

- 依固定順序整理：書目（APA 7th）、一句話主張、研究問題、理論視角、研究設計、核心發現、**機制**、邊界條件、審稿人視角。
- 先判斷文章類型（質性實證、量化實證、概念文章、文獻回顧、實務文章），用對應的標準評估，不拿量化標準批評質性研究。
- 質性文章依 Yin、Eisenhardt、Gioia、主題分析、過程研究等傳統檢核方法交代是否完整。
- 引文一律逐字並附頁碼；不確定就改成轉述。書目缺漏寫「待查證」，不憑記憶補。
- 內容分成【作者主張】【證據】【我的詮釋】三種標記。
- 填好 `my-research.md` 後，會判斷這篇和你論文的關係（支持、延伸、衝突、方法參照），並指向你的章節。
- 每篇另外產生一行文獻矩陣（CSV），之後做綜述時可以直接彙整。

## 檔案結構

```
close-reading/                      ← skill 本體（上傳或複製這個資料夾）
├── SKILL.md
├── references/
│   ├── my-research.md              ← 請填你自己的研究
│   └── qual-methods-checklist.md
├── scripts/
│   └── verify_quotes.py            ← 比對精讀卡引文是否逐字存在於 PDF
└── templates/
    ├── reading-card.md
    └── matrix-row.md
dist/close-reading.zip              ← 已打包好，可直接上傳 claude.ai
examples/                           ← 測試產出的精讀卡與文獻矩陣範例
```

## 範例與測試

`examples/` 是用兩篇不同性質的文獻實際跑出來的結果（`my-research.md` 空白時的通用模式）：

| 文獻 | 類型 | 測試重點 |
|---|---|---|
| Adner (2017), *Journal of Management* | 同儕審查概念文章 | 線上搶先版 2016 與正式卷期 2017 的年份判斷；PDF 頁序與期刊頁碼差 38 的換算；6 則引文全部通過程式比對 |
| Pidun, Reeves, & Knust (2021), BCG | 顧問實務報告 | 辨識實務文章、不當作實證證據；偵測到 PDF 第 6–11 頁的「EARLY DRAFT—INTERNAL BCG USE ONLY」並發出版本警示；5 則引文全部通過比對 |

自行核對引文（需安裝 poppler 的 `pdftotext`）：
```bash
python close-reading/scripts/verify_quotes.py 論文.pdf 精讀卡.md
```

## 安裝

### 1. 先填寫你的研究
打開 `close-reading/references/my-research.md`，填入你的題目、研究問題、資料來源、理論視角和真實章節。
沒填也能用，只是無法對應到你自己的論文。

### 2a. claude.ai（網頁、桌面版、手機 App）
1. 下載 `dist/close-reading.zip`。若有修改 `my-research.md`，請把 `close-reading` 資料夾重新壓縮成 zip。
2. 到 claude.ai 設定中的 Skills 區上傳 zip。
3. 新對話中上傳 PDF，說「精讀這篇」。

### 2b. Claude Code
```bash
git clone https://github.com/whocare-lab/close-reading-claude.git
# macOS / Linux
cp -R close-reading-claude/close-reading ~/.claude/skills/
# Windows（PowerShell）
Copy-Item -Recurse close-reading-claude\close-reading $env:USERPROFILE\.claude\skills\
```
在 Claude Code 中，精讀卡存到目前專案的 `literature/cards/`，文獻矩陣附加到 `literature/matrix.csv`。

## 使用時請注意

- 精讀卡是閱讀輔助，**不是可以直接引用的來源**。正式引用前，請回原文核對引文和頁碼。
- 若 PDF 是掃描檔或文字抽取有亂碼，引文準確度會下降；skill 會改用轉述並標註。
- 不要把未公開的訪談逐字稿或受訪者資料寫進 `my-research.md` 後再公開分享。

## 授權

MIT License。歡迎同學 fork 後依自己的研究調整。
