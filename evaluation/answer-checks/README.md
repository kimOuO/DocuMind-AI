# answer-checks — 句級檢查在真實回答上的回放（D68）

D67 之後三題的剩餘缺口不在數字本身：Q3 的數字全對，結尾卻寫「在所有資料集與指標都優於消融版本」；Q2 把第 10 頁才有的更新機制說明引到第 9 頁的成本數字。這個實驗用 19 份保存下來、附來源清單的真實回答（13 份改版前、6 份改版後的回歸），量測兩個新加的句級檢查，對照人工標註。

## 兩個檢查

| 檢查 | 看什麼 | 怎麼判 | 輸出 |
|---|---|---|---|
| 全稱比較宣稱 `check_universal_claims` | 一句同時有全稱詞（consistently／in all cases／across all…；中文 全面／所有／都…）、比較動詞（outperform／better／higher…；優於／勝過…），且比較動詞前有表格裡的方法名 | 在引用頁面的表格裡，找主詞與比較對象共享（列、分組）的格子，數主詞較高與較低的格數。**兩邊都有** → 不論指標方向都不成立 → 不符，附較少那一方向的格子為反例。全部同方向 → 不報（不假設高好或低好）。沒有共享格子 → 無法判定 | `done.overstated_claims`；不符者在回答後附說明 |
| 引用可疑 `check_citations` | 每句有引用的陳述 | 內容詞（含數字）對每個來源算覆蓋率：被引來源最高 ≤ 0.34、某未被引來源 ≥ 0.5 且 ≥ 3 個共同詞、≥ 被引兩倍 → 可疑。被引來源含該句數字、或較接近的來源與被引同頁 → 不算 | `done.doubtful_citations`；只在展開細節灰字顯示 |

細節規則：bare 的「all／every」可能只涵蓋一個未說出的切面（「in all evaluation dimensions」可能是說某一資料集或案例研究），所以只有在**沒有任何一列或一欄位分組**是單一方向時才判不符；「consistently」「across all」等不留這個餘地。帶 most／nearly／particularly／especially 等限定詞的句子不算全稱。

## 資料

- `answers.json`：19 份真實回答（Q3 ×13、Q2 ×6；C14–C19 是 D68 改版後用新提示詞跑的回歸），每份附模型看到的來源清單（編號、頁、來源種類、切塊開頭）與回答引用的編號。回放時用專案設定重新切塊論文，依頁與開頭對回切塊全文，所以檢查看到的就是模型看到的。Q1 的來源是摘要而非切塊，不在此回放。
- `labels.json`：人工標註——哪些句子是表格不支持的全稱宣稱、哪些有引用的句子引到了別頁（頁級判準，與 key-facts 一致）。附判斷理由。
- `results.json`：每份回答的候選句、檢查輸出與彙整。

## 結果（2026-11-06）

| | 全稱比較宣稱 | 引用可疑 |
|---|---|---|
| 候選句（有全稱＋比較詞） | 8 | — |
| 人工標為錯 | 3 | 13 |
| TP | 3 | 12 |
| FP | 0 | 0 |
| FN | 0 | 1 |
| 無法判定 | 0 | — |

抓到的 3 個全稱宣稱：C01、C12 的「the hybrid mode … consistently outperforms the ablated versions across all datasets and metrics」（反例：Comprehensiveness／Agriculture LightRAG 67.6% 對 -Origin 75.2%、Comprehensiveness／Mix 61.2% 對 -Low 64.0% 等），C09 的「consistently balances breadth and depth, outperforming all variants」。沒誤報的 3 句：「outperforming NaiveRAG (32.4%–38.8%) across all datasets」（Comprehensiveness 列確實全高）；「consistently outperforms GraphRAG, particularly in larger datasets」（有 particularly，論文原句）；「in all evaluation dimensions assessed by the LLM judge」（說的是案例研究；Agriculture 整欄單向，故不判）。

抓到的 12 個可疑引用大多是同一個模式：更新機制「GraphRAG must dismantle its existing community structure …」及其結果寫在第 10 頁（來源 [5]），六份 Q2 回答裡有五份引到第 9 頁的成本數字 [3]（或整段只在段尾引一次 [3]）；另有 Q3 把 hybrid mode 的說明引到第 7 頁的 [2]、Q2 把第 7 頁的「disparity … significant」引到第 8 頁的 [4]、C17 把 -Origin 的改善寫成 GraphRAG 的（事實錯誤，連引用一起錯）。沒誤報的：「1,399 × 2 × 5,000 tokens … [3]」——數字就在 [3]；Q3 把說明句引到同頁的表格切塊 [1]——同頁不算；Q1 的摘要來源不在檢查範圍。1 個漏報：C15「In contrast, GraphRAG must dismantle … 5,000 tokens per community report」——機制在第 10 頁、數字在第 9 頁，同一句混用，數字在被引來源就不懷疑（設計上的取捨）。

## 調整過程（誠實記錄）

- 第一輪回放：全稱宣稱 FP 8、引用可疑 FP 17。原因：(1) 「particularly」沒被當限定詞；(2) bare「all」被當全範圍；(3) 反例全部來自第一張表（Table 1 的 GraphRAG），而句子說的是消融版本；(4) 引用檢查沒把數字當內容詞、也沒排除同頁。
- 修正：限定詞加 particularly／especially；bare「all」改為切面規則；反例跨表輪流取；數字算內容詞、同頁來源算被引、被引來源含該句數字不算可疑；最少內容詞由 5 降到 4（讓 C11 的短句進入檢查）。
- 改版後的 6 份回歸回答加入後再修兩處：沒有自己引用的句子沿用同段下一個引用（模型常整段只引一次）；同頁來源的覆蓋算進被引（Q3 把說明句引到同頁表格不算錯）。標註也依頁面重讀改過：C19 的「1,399 × 2 × 5,000 … [5]」原標為錯，第 10 頁內文也寫了這個數字，改為對。
- 門檻（0.34／0.5／3 個共同詞／兩倍／4 個詞）是在這 19 份回答上選的，樣本小；其中 6 份是改版後的回歸，檢查的最後兩處修正是看了它們才加的，所以這 6 份不是乾淨的測試集。

## 限制

- 全稱宣稱只對引用頁面上、依第 5 節格式線性化的表格有效；表格以外的全稱（「in all case studies」）查不到。方法名變體（「Naive RAG」）認不出。比較對象沒點名時取表格裡所有其他方法，反例可能來自句子沒打算比的那張表（已改為跨表輪流列出，但不能排除）。
- 引用可疑是字面比對：改寫、同義詞抓不到；只抓明顯錯配；中文句子不檢查；只對原文切塊來源（摘要來源是改寫，不檢查）；一句同時含被引來源的數字與別頁的說明時不懷疑。它不證明任何引用是對的。
- 兩個檢查都只標示，不修正回答；AC-13、AC-14 仍以回答內容判定。

## 重現

```bash
.venv/bin/python evaluation/answer-checks/replay.py
```

需要 `sample-documents/2410.05779v3.pdf`。
