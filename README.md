# close-reading｜管理學質性研究英文文獻精讀 Skill

**繁體中文** ｜ [English](README.en.md)

給管理學院做質性研究、個案研究的同學使用的 Claude skill。
上傳一篇英文文獻 PDF，說「精讀這篇」，Claude 會產出可以回原文核對的精讀素材。

> **下一步：多篇文獻綜述整合**
> 精讀完多篇之後，用 [whocare-lab/overview-reading](https://github.com/whocare-lab/overview-reading) 的 `lit-synthesis` skill，把精讀卡與 `matrix.csv` 整合成概念矩陣、論證大綱、研究缺口與文獻探討初稿。

## 三種產出

| 產出 | 內容 | 怎麼觸發 |
|---|---|---|
| **A. 精讀卡**（每次都做） | 核心主張、研究問題、理論框架、研究方法、研究發現、機制、研究貢獻、研究限制、**論文心智圖**、**智慧標註清單**、關鍵引文、與你論文的關係、審稿人視角 | 「精讀這篇」 |
| **B. 彩色標註 PDF** | 在原 PDF 副本上畫螢光標記，點選可看中文註記；原檔不動 | 精讀時自動產出（需能執行 Python） |
| **C. 逐段中英對照** | 英文原文一段、中文譯文一段，附術語對照表與節名頁碼 | 「做中英對照」「逐段翻譯對照」 |

### 智慧標註的固定顏色

| 顏色 | 意義 |
|---|---|
| 🟨 黃 | 核心概念與主要主張 |
| 🟩 綠 | 方法、研究設計、分析架構 |
| 🟦 藍 | 證據、資料、研究發現與數據 |
| 🟥 紅 | 限制、邊界條件、待研究問題 |

### 論文心智圖
以 Mermaid 語法產出，GitHub、Obsidian、Typora、claude.ai 都能直接顯示；第一層固定為研究問題、理論框架、研究方法、研究發現、研究貢獻、研究限制。

## 品質保證

- **引文逐字核對**：`scripts/verify_quotes.py` 會把精讀卡的每則引文、每段標註，以及中英對照檔的每段英文原文，逐一比對 PDF。比對會自動忽略換行、斷字、首字放大、頁首頁尾；跨頁被註腳或表格打斷的段落也能比對，但任何一個字的增刪改都會被抓出來。
- 引文一律附印出頁碼，並自動換算 PDF 頁序與期刊頁碼的差距。
- 書目缺漏寫「待查證」，不憑記憶補；偵測草稿、預印本等版本狀態並發出警示。
- 依文章類型（質性實證、量化實證、概念文章、文獻回顧、實務文章）使用對應的評估標準。
- 內容分成【作者主張】【證據】【我的詮釋】三種標記。

## 輸出語言

預設繁體中文。用英文提問，或說「English」「英文版」，精讀卡就改用英文撰寫；中英對照仍是英文原文配中文譯文。

## 檔案結構

```
close-reading/                      ← skill 本體（上傳或複製這個資料夾）
├── SKILL.md
├── references/
│   ├── my-research.md              ← 請填你自己的研究
│   └── qual-methods-checklist.md
├── scripts/
│   ├── verify_quotes.py            ← 逐字比對引文與對照原文
│   └── annotate_pdf.py             ← 產生彩色標註 PDF
└── templates/
    ├── reading-card.md
    └── matrix-row.md
dist/close-reading.zip              ← 已打包好，可直接上傳 claude.ai
examples/                           ← 測試產出的精讀卡與文獻矩陣範例
```

## 安裝

### 1. 先填寫你的研究
打開 `close-reading/references/my-research.md`，填入題目、研究問題、資料來源、理論視角與真實章節。沒填也能用，只是無法對應到你自己的論文。

### 2a. claude.ai（網頁、桌面版、手機 App）
1. 下載 `dist/close-reading.zip`。若修改了 `my-research.md`，請把 `close-reading` 資料夾重新壓縮成 zip。
2. 到 claude.ai 設定中的 Skills 區上傳 zip。
3. 新對話中上傳 PDF，說「精讀這篇」或「做中英對照」。

### 2b. Claude Code
```bash
git clone https://github.com/whocare-lab/close-reading.git
# macOS / Linux
cp -R close-reading/close-reading ~/.claude/skills/
# Windows（PowerShell）
Copy-Item -Recurse close-reading\close-reading $env:USERPROFILE\.claude\skills\
# 腳本需要的套件
pip install pypdf pypdfium2
```
產出存到目前專案的 `literature/`：精讀卡在 `cards/`、標註 PDF 在 `annotated/`、對照在 `bilingual/`，文獻矩陣附加到 `literature/matrix.csv`。

## 範例與測試

用兩篇性質不同的文獻實際測試（`my-research.md` 空白時的通用模式）：

| 文獻 | 類型 | 結果 |
|---|---|---|
| Adner (2017), *Journal of Management* | 同儕審查概念文章 | 正確判斷線上搶先版 2016 與正式卷期 2017；算出 PDF 頁序與期刊頁碼差 38；精讀卡 22 則引文與標註、標註 PDF 17 處、全文對照 95 段英文，全部通過逐字比對 |
| Pidun, Reeves, & Knust (2021), BCG | 顧問實務報告 | 判定為實務文章、不當作實證證據；偵測到第 6–11 頁的「EARLY DRAFT—INTERNAL BCG USE ONLY」並發出版本警示；精讀卡 16 則、標註 PDF 11 處、全文對照 64 段，全部通過比對 |

比對工具另以 9 種竄改測試（改一個字、改數字、刪一個子句、句尾加字等）驗證，全部能抓出來。

`examples/` 只放精讀卡與文獻矩陣。**全文中英對照與標註 PDF 含原文全文，基於著作權不公開放在 repo 中**；請用自己合法取得的 PDF 產出，僅供個人閱讀。

自行核對（需安裝 `pdftotext` 或 `pypdfium2`）：
```bash
# --offset：印出頁碼＝PDF 頁序＋差值（例如 PDF 第 1 頁＝期刊第 39 頁，差值 38）；加上後會一併檢查引文旁的頁碼
python close-reading/scripts/verify_quotes.py --offset 38 論文.pdf 精讀卡或對照檔.md
```

## 使用時請注意

- 精讀卡與譯文是閱讀輔助，**不是可以直接引用的來源**。論文中請引英文原文與頁碼。
- 掃描檔或文字抽取有亂碼的 PDF，引文準確度會下降；skill 會改用轉述並標註。
- 不要把未公開的訪談逐字稿或受訪者資料寫進 `my-research.md` 後再公開分享。

## 致謝與授權

逐段對照、固定顏色的智慧標註與論文心智圖的構想，參考自 [YuriyLin/PaperRead](https://github.com/YuriyLin/PaperRead)（MIT License）。本 repo 未使用其程式碼，以 Claude skill 的形式重新實作，並針對管理學質性研究調整。

MIT License。歡迎同學 fork 後依自己的研究調整。
