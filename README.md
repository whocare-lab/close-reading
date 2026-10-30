# close-reading｜精讀 Skill・Gemini 版（`gemini` 分支）

> ⚠️ **這是 Gemini 專用分支。**
> Claude（claude.ai、Claude Code）與 ChatGPT 請用 [main 分支](https://github.com/whocare-lab/close-reading/tree/main) 的原版 `dist/close-reading.zip`，**不要用這一版**。
> 兩個版本各自維護、不互相合併。

## 為什麼要分出 Gemini 版

Gemini 能載入 skill 的說明與模板，但**不會執行 skill 內的 Python 程式**（會回覆「目前此環境暫不支援直接執行該外掛腳本」——這是平台限制，不是安裝錯誤）。
因此本版：

| 項目 | main（Claude／ChatGPT） | gemini（本分支） |
|---|---|---|
| 精讀卡、心智圖、智慧標註清單 | 產出 `.md` 檔 | 直接呈現在對話中 |
| 逐段中英對照 | 產出 `.md` 檔 | 在對話中分批呈現 |
| 彩色標註 PDF | `annotate_pdf.py` 自動產出 | **不產出**（精讀卡內仍有四色標註清單） |
| 引文逐字核對 | `verify_quotes.py` 程式比對 | Gemini 逐則人工核對，並標「未經程式比對」 |
| 要 PDF | — | 回覆下方「匯出至 Google 文件」→ 從 Google 文件下載 PDF |
| 品質規則（APA、頁碼對應、版本警示、逐字引文、禁止事項） | ✅ | ✅ 完全相同 |

## 安裝（Gemini 網頁版或手機瀏覽器 gemini.google.com）

1. 下載本分支的 [`dist/close-reading-gemini.zip`](https://github.com/whocare-lab/close-reading/raw/gemini/dist/close-reading-gemini.zip)。
2. 想讓精讀對應到你自己的論文：解壓後填寫 `close-reading/references/my-research.md`，再把 `close-reading` 資料夾重新壓縮成 zip。
3. 在 Gemini 的技能設定上傳 zip。
4. 新對話上傳 PDF，說「精讀這篇」或「做中英對照」。

## 使用時請注意

- 引文只經 AI 人工核對，**正式引用前請自己再對照原文與頁碼**。需要程式逐字比對與彩色標註 PDF，請改用 Claude 版。
- 精讀卡與譯文是閱讀輔助，不是可以直接引用的來源。論文中請引英文原文與頁碼；全文譯本不要公開散布。
- 不要把未公開的訪談逐字稿或受訪者資料寫進 `my-research.md` 後再分享。

## 授權

MIT License。構想致謝與完整說明見 [main 分支 README](https://github.com/whocare-lab/close-reading/blob/main/README.md)。
