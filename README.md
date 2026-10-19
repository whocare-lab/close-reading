# close-reading｜管理學質性研究文獻精讀與綜述 Skills

**繁體中文** ｜ [English](README.en.md)

給管理學院做質性研究、個案研究的同學使用的兩個 Claude skill，從讀懂一篇到寫出文獻探討：

```
英文文獻 PDF ──► close-reading（一次一篇）──► 精讀卡＋文獻矩陣 ──► lit-synthesis（多篇）──► 概念矩陣、論證大綱、研究缺口、文獻探討初稿
```

| Skill | 用途 | 怎麼觸發 |
|---|---|---|
| **close-reading** | 精讀一篇英文文獻，產出可回原文核對的精讀卡 | 上傳 PDF，說「精讀這篇」 |
| **lit-synthesis** | 把多篇精讀結果整合成有論證脈絡的文獻探討 | 說「整合這些文獻」「幫我寫文獻探討」「整理研究缺口」 |

兩個可以分開安裝；建議兩個都裝，因為 lit-synthesis 的最佳輸入就是 close-reading 的精讀卡。

---

## Skill 1：close-reading（單篇精讀）

### 三種產出

| 產出 | 內容 | 怎麼觸發 |
|---|---|---|
| **A. 精讀卡**（每次都做） | 核心主張、研究問題、理論框架、研究方法、研究發現、機制、研究貢獻、研究限制、**論文心智圖**、**智慧標註清單**、關鍵引文、與你論文的關係、審稿人視角 | 「精讀這篇」 |
| **B. 彩色標註 PDF** | 在原 PDF 副本上畫螢光標記，點選可看中文註記；原檔不動 | 精讀時自動產出（需能執行 Python） |
| **C. 逐段中英對照** | 英文原文一段、中文譯文一段，附術語對照表與節名頁碼 | 「做中英對照」「逐段翻譯對照」 |

智慧標註的固定顏色：🟨 黃＝核心概念與主張｜🟩 綠＝方法與研究設計｜🟦 藍＝證據與發現｜🟥 紅＝限制與待研究問題。

### 品質保證
- **引文逐字核對**：`verify_quotes.py` 把精讀卡的每則引文、每段標註，以及中英對照的每段英文，逐一比對 PDF。會自動忽略換行、斷字、首字放大、頁首頁尾；跨頁被註腳或表格打斷的段落也能比對，但任何一個字的增刪改都會被抓出來。
- 引文附印出頁碼，自動換算 PDF 頁序與期刊頁碼的差距。
- 書目缺漏寫「待查證」；偵測草稿、預印本等版本狀態並警示。
- 依文章類型（質性實證、量化實證、概念、回顧、實務文章）使用對應的評估標準。

---

## Skill 2：lit-synthesis（多篇綜述整合）

### 產出

| 產出 | 內容 |
|---|---|
| **A. 概念矩陣** | 文獻清單、覆蓋度檢查（年代、方法、情境、分析層次、理論、證據強度）、文獻 × 概念矩陣（每格附頁碼）、讀矩陣看到的模式 |
| **B. 論證大綱** | 漏斗式章節結構，每節一句主張、每段主題句與支持文獻、節與節的銜接；附 Mermaid 文獻地圖與建議補讀清單 |
| **C. 研究缺口陳述** | 每個缺口標出類型（混淆、忽略、應用、問題化），附矩陣證據，並說明缺什麼、為什麼重要、你的研究怎麼補 |
| **D. 文獻探討初稿**（要求才做） | 以概念為主語的學術段落、APA 7th 引用、參考文獻清單 |

### 它和「請 AI 寫文獻探討」有什麼不同
- **以概念組織，不以作者組織**：不會寫成「A 認為……。B 認為……」的列表。
- **每個主張至少兩篇來源**，只有一篇時標「單一來源」；分歧一定要解釋原因。
- **只用你提供的文獻**：你沒讀過的文獻只會出現在「建議補讀」，不會混進正文。
- **缺口不寫空話**：「目前相關研究較少」「本研究填補此一缺口」這類句子，沒有具體證據就會被改寫。
- **文獻量不足會警告**：少於 5 篇標「初步整合」，少於 3 篇不下缺口定論。
- **引用檢查程式** `check_citations.py`：檢查文內引用與參考文獻是否一一對應、引用的文獻是否都有精讀卡（抓出憑記憶加入的文獻）、APA 7 的 et al. 寫法是否一致。中英文引用都支援。

---

## 輸出語言
預設繁體中文。用英文提問，或說「English」「英文版」，就改用英文撰寫。

## 檔案結構

```
close-reading/                      ← Skill 1（上傳或複製這個資料夾）
├── SKILL.md
├── references/  my-research.md、qual-methods-checklist.md
├── scripts/     verify_quotes.py、annotate_pdf.py
└── templates/   reading-card.md、matrix-row.md
lit-synthesis/                      ← Skill 2
├── SKILL.md
├── references/  my-research.md、synthesis-methods.md
├── scripts/     check_citations.py、verify_quotes.py
└── templates/   concept-matrix.md、review-outline.md、gap-statement.md
dist/close-reading.zip              ← 打包好的 Skill 1，可直接上傳 claude.ai
dist/lit-synthesis.zip              ← 打包好的 Skill 2
examples/                           ← 精讀卡、文獻矩陣與綜述整合的測試產出
```

## 安裝

### 1. 先填寫你的研究
打開 `close-reading/references/my-research.md`，填入題目、研究問題、資料來源、理論視角與真實章節，再把同一份內容複製到 `lit-synthesis/references/my-research.md`。lit-synthesis 需要知道你的研究問題才能判斷缺口；沒填時它會先問你一個問題。

### 2a. claude.ai（網頁、桌面版、手機 App）
1. 下載 `dist/close-reading.zip` 與 `dist/lit-synthesis.zip`。若修改了 `my-research.md`，請把對應資料夾重新壓縮成 zip。
2. 到 claude.ai 設定中的 Skills 區，分別上傳兩個 zip。
3. 新對話中：
   - 上傳一篇 PDF，說「精讀這篇」。
   - 上傳多張精讀卡（或 `matrix.csv`），說「整合這些文獻，研究問題是……」。

### 2b. Claude Code
```bash
git clone https://github.com/whocare-lab/close-reading-claude.git
# macOS / Linux
cp -R close-reading-claude/close-reading close-reading-claude/lit-synthesis ~/.claude/skills/
# Windows（PowerShell）
Copy-Item -Recurse close-reading-claude\close-reading, close-reading-claude\lit-synthesis $env:USERPROFILE\.claude\skills\
# 腳本需要的套件
pip install pypdf pypdfium2
```
產出存到目前專案的 `literature/`：精讀卡在 `cards/`、標註 PDF 在 `annotated/`、對照在 `bilingual/`、綜述在 `synthesis/`，文獻矩陣在 `literature/matrix.csv`。

## 範例與測試

### close-reading
| 文獻 | 類型 | 結果 |
|---|---|---|
| Adner (2017), *Journal of Management* | 同儕審查概念文章 | 正確判斷線上搶先版 2016 與正式卷期 2017；算出頁碼差 38；精讀卡 22 則引文與標註、標註 PDF 17 處、全文對照 95 段，全部通過逐字比對 |
| Pidun, Reeves, & Knust (2021), BCG | 顧問實務報告 | 判定為實務文章；偵測到第 6–11 頁的內部草稿標記並警示；精讀卡 16 則、標註 PDF 11 處、全文對照 64 段，全部通過比對 |

比對工具另以 9 種竄改測試（改一個字、改數字、刪一個子句、句尾加字等）驗證，全部能抓出來。

### lit-synthesis
以上述兩張精讀卡整合，示範研究問題為「協調者如何透過治理設計，促成生態系夥伴的對齊？」，產出放在 `examples/synthesis/`：
- 正確觸發文獻量警示（2 篇，少於 3 篇），缺口只寫成「初步觀察」。
- 覆蓋度檢查指出：實證研究 0 篇、沒有非營利或教育情境、兩篇分析單位不同。
- 找出一個分歧（治理是「設計」還是「協商」）並解釋原因，一個共同前提（都假設有單一焦點行動者）。
- 初稿的 8 次文內引用與參考文獻清單完全對應；2 則直接引文分別在兩篇 PDF 中逐字找到。
- 引用檢查程式另以測試檔驗證：能抓出漏列的參考文獻、未被引用的參考文獻、沒有精讀卡的文獻、三位以上作者未寫 et al.。

**兩篇只是示範**，真正的文獻探討需要更多文獻；skill 會在文獻量不足時提醒你。

`examples/` 不放全文中英對照與標註 PDF：它們含原文全文，基於著作權不公開；請用自己合法取得的 PDF 產出，僅供個人閱讀。

### 自行核對
```bash
python close-reading/scripts/verify_quotes.py 論文.pdf 精讀卡或對照檔.md
python lit-synthesis/scripts/verify_quotes.py 文獻1.pdf 文獻2.pdf 文獻探討初稿.md
python lit-synthesis/scripts/check_citations.py 文獻探討初稿.md literature/matrix.csv
```

## 使用時請注意
- 精讀卡、譯文與文獻探討初稿都是輔助，**不是可以直接引用或繳交的成品**。論文中請引英文原文與頁碼，初稿請用自己的語言改寫。
- 「尚未有研究探討」是很強的宣稱。skill 只能根據你提供的文獻判斷，定稿前請自行補檢索。
- 掃描檔或文字抽取有亂碼的 PDF，引文準確度會下降。
- 不要把未公開的訪談逐字稿或受訪者資料寫進 `my-research.md` 後再公開分享。

## 致謝與授權
close-reading 的逐段對照、固定顏色智慧標註與論文心智圖構想，參考自 [YuriyLin/PaperRead](https://github.com/YuriyLin/PaperRead)（MIT License）；本 repo 未使用其程式碼。lit-synthesis 的方法依據見 `lit-synthesis/references/synthesis-methods.md`。

MIT License。歡迎同學 fork 後依自己的研究調整。
