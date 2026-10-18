# 文獻矩陣紀錄格式

每精讀一篇，產生一行 CSV，供之後的「文獻綜述整合」使用。
欄位內有逗號時用雙引號包起來。

## 表頭（matrix.csv 第一行）

```
id,apa_short,year,journal,article_type,tradition,theory,unit_of_analysis,data_sources,analysis_method,key_finding,mechanism,boundary,relation_to_my_paper,my_paper_section,priority,to_verify,card_file
```

## 欄位說明

| 欄位 | 內容 |
|---|---|
| id | 第一作者_年份，例：Smith_2020 |
| apa_short | 文內引用格式，例：Smith & Lee, 2020 |
| year | 出版年 |
| journal | 期刊名 |
| article_type | 質性實證／量化實證／概念／回顧 |
| tradition | Yin／Eisenhardt／Gioia／主題分析／過程／其他／不適用 |
| theory | 主要理論 |
| unit_of_analysis | 分析單位 |
| data_sources | 資料來源與數量 |
| analysis_method | 分析方法 |
| key_finding | 核心發現（一句） |
| mechanism | 機制（一句） |
| boundary | 邊界條件（一句） |
| relation_to_my_paper | confirm／extend／contradict／method／low |
| my_paper_section | 對應我的論文章節 |
| priority | 核心／輔助／方法／略過 |
| to_verify | 待查證項目，沒有則留空 |
| card_file | 精讀卡檔名 |
