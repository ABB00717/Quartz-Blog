---
title: 00 死結（Deadlocks）
draft: false
tags:
  - operating-systems
date: 2025-12-10
---

**死結**是指一組被阻塞（Blocked）的行程（Process），其中每個行程都持有一個資源，並等待獲取該組中另一個行程所持有的資源 。

# 大綱
- 為了分析死結，把系統資源抽象化成系統模型
- 分析死結的四大必要因素
- 如何預防上述四大因素
- 如何在動態系統中避免死結
- 如何檢測動態系統中是否有死結
- 檢測到死結後，應當如何恢復

---

# 系統模型 (System Model)

為了分析死結，我們將系統資源抽象化。系統包含有限數量的資源，分為多種資源類型（Resource Types）$R_1, R_2, ..., R_m$（如 CPU 週期、記憶體空間、I/O 裝置）。

行程在使用資源時，遵循以下順序：
1.  **請求 (Request)**：若資源無法立即獲得，行程會被阻塞，直到獲得資源 。
2.  **使用 (Use)**：行程對資源進行操作 。
3.  **釋放 (Release)**：行程釋放資源 。

## 資源分配圖 (Resource-Allocation Graph, RAG)
死結狀態可透過有向圖（Directed Graph）來描述。圖形包含頂點集合 $V$ 與邊集合 $E$ ：
* **頂點 (Vertices)**：
    * $P = \{P_1, ..., P_n\}$：系統中所有行程的集合 。
    * $R = \{R_1, ..., R_m\}$：系統中所有資源類型的集合 。
* **邊 (Edges)**：
    * **請求邊 (Request Edge)**：$P_i \rightarrow R_j$，表示行程 $P_i$ 請求資源 $R_j$ 的一個實例 。
    * **分配邊 (Assignment Edge)**：$R_j \rightarrow P_i$，表示資源 $R_j$ 的一個實例已分配給行程 $P_i$ 。

![[image-14.png]]

若資源分配圖中不包含循環（Cycle），則系統無死結 。若圖中包含循環：
* 若每種資源類型只有一個實例，則必有死結 。
* 若資源類型有多個實例，則**可能**有死結 。

# 死結特徵 (Deadlock Characterization)

死結的發生必須同時滿足以下四個條件 ：

1.  **互斥 (Mutual Exclusion)**：至少有一個資源必須處於非共享模式，即同一時間只有一個行程能使用該資源 。
2.  **持有並等待 (Hold and Wait)**：一個行程必須至少持有一個資源，並正在等待獲取其他行程持有的額外資源 。
3.  **不可搶佔 (No Preemption)**：資源不能被搶佔；資源只能在行程完成任務後自願釋放 。
4.  **循環等待 (Circular Wait)**：存在一組等待行程 $\{P_0, P_1, ..., P_n\}$，使得 $P_0$ 等待 $P_1$ 持有的資源，$P_1$ 等待 $P_2$ ...，$P_{n-1}$ 等待 $P_n$，且 $P_n$ 等待 $P_0$ 持有的資源 。

# 死結預防 (Deadlock Prevention)

死結預防的策略是確保上述四個必要條件中至少有一個不成立 。

* **破除互斥**：對於不可共享的資源（如印表機），互斥條件必須成立，因此通常無法透過此條件預防 。
* **破除持有並等待**：
    * 要求行程在執行前一次請求並獲分配所有資源 。
    * 或要求行程僅在未持有任何資源時才能請求資源（需先釋放現有資源）。
    * 缺點：資源利用率低，且可能導致飢餓（Starvation）。
* **破除不可搶佔**：
    * 若一個持有資源的行程請求新資源被拒絕（需等待），則該行程持有的所有資源將被搶佔（隱式釋放）。
    * 此方法通常適用於狀態易於保存與恢復的資源（如 CPU 暫存器、記憶體）。
* **破除循環等待**：
    * 對所有資源類型進行全序排序（Total Ordering），要求每個行程必須按照遞增順序請求資源 。
    * 例如：若磁碟排序為 4，印表機為 8，持有磁碟的行程可以請求印表機，但不能請求順序比磁碟低的資源（如磁帶）。

詳細請閱讀：[[deadlock-prevention |死結預防]]

# 死結避免 (Deadlock Avoidance)

死結避免要求系統擁有額外的先驗資訊（A priori information），最簡單的模型是要求每個行程宣告其可能需要的各類資源的**最大需求量 (Maximum Claim)** 。

也就是說，系統**動態執行**過程中，根據當前和未來的資源需求資訊，**有條件地**允許資源分配，確保系統始終處於「安全狀態」，從而避免進入可能導致死結的「不安全狀態」。

## 安全狀態 (Safe State)
* 若系統能找到一個行程執行的序列 $<P_1, P_2, ..., P_n>$，使得對於每個 $P_i$，其尚需的資源可由「目前可用資源」加上「所有 $P_j (j < i)$ 持有的資源」來滿足，則系統處於**安全狀態** 。
* **安全狀態** $\Rightarrow$ 無死結 。
* **不安全狀態 (Unsafe State)** $\Rightarrow$ **可能**發生死結 。
* 避免演算法的核心即是確保系統永遠不會進入不安全狀態 。

詳細請閱讀：[[safe state | 安全狀態]]

## 銀行家演算法 (Banker's Algorithm)
適用於多重實例資源類型的死結避免演算法 。

### 資料結構
設 $n$ 為行程數，$m$ 為資源種類數：
* **Available**：長度為 $m$ 的向量，表示各類資源的可用數量 。
* **Max**：$n \times m$ 矩陣，$Max[i,j]$ 表示行程 $P_i$ 對資源 $R_j$ 的最大需求 。
* **Allocation**：$n \times m$ 矩陣，表示行程 $P_i$ 目前已持有的資源量 。
* **Need**：$n \times m$ 矩陣，表示行程 $P_i$ 還需要多少資源，$Need[i,j] = Max[i,j] - Allocation[i,j]$ 。

### 安全性演算法 (Safety Algorithm)
用於檢查系統是否處於安全狀態：
1.  初始化 `Work = Available`，`Finish[i] = false` (對於所有 $i$) 。
2.  尋找一個 $i$ 滿足：`Finish[i] == false` 且 `Need_i <= Work` 。
3.  若找到，則假設該行程完成並釋放資源：`Work = Work + Allocation_i`，`Finish[i] = true`，回到步驟 2 。
4.  若所有 `Finish[i]` 皆為 `true`，則系統處於安全狀態 。

### 資源請求演算法 (Resource-Request Algorithm)
當行程 $P_i$ 提出請求 `Request_i`：
1.  若 `Request_i > Need_i`，則報錯（請求超過宣告的最大值）。
2.  若 `Request_i > Available`，則 $P_i$ 必須等待 。
3.  **試探性分配**：修改系統狀態：
    * `Available = Available - Request_i`
    * `Allocation_i = Allocation_i + Request_i`
    * `Need_i = Need_i - Request_i` 。
4.  執行安全性演算法。若結果為安全，則正式分配；若不安全，則還原狀態，$P_i$ 等待 。

詳細請閱讀：[[banker-algo | 銀行家演算法]]

# 死結檢測 (Deadlock Detection)

若系統不使用預防或避免機制，則需提供檢測演算法與恢復機制 。

## 單一實例資源
* 使用**等待圖 (Wait-for Graph)**：這是資源分配圖的變形，移除了資源節點，直接將行程節點相連。若 $P_i \rightarrow P_j$，表示 $P_i$ 等待 $P_j$ 。
* 若等待圖中存在循環，則系統存在死結 。

![[image-13.png]]

## 多重實例資源 (Detection Algorithm)
類似於銀行家演算法，但使用 **Request** 矩陣代替 Max 。
1.  初始化 `Work = Available`。若 `Allocation_i` 不為 0，則 `Finish[i] = false`，否則為 `true` 。
2.  尋找一個 $i$ 滿足：`Finish[i] == false` 且 `Request_i <= Work` 。
3.  若找到，執行 `Work = Work + Allocation_i`，`Finish[i] = true`，回到步驟 2 。
4.  若最終存在 `Finish[i] == false`，則該行程 $P_i$ 處於死結狀態 。

**檢測頻率**：應視死結發生的可能頻率與影響範圍而定。若死結頻發，應頻繁檢測（例如當 CPU 利用率低於 40% 時）。

詳細請閱讀：[[detection-algo | 死結檢測]]

# 死結恢復 (Recovery from Deadlock)

一旦檢測到死結，系統可透過以下方式恢復：

## 行程終止 (Process Termination)
* **終止所有死結行程** 。
* **一次終止一個行程**：直到死結循環消除。選擇受害者的依據包括：優先權、已執行時間、已使用資源量、完成所需資源量等 。

## 資源搶佔 (Resource Preemption)
從行程中搶佔資源分配給其他行程，直到打破死結 。
* **選擇受害者 (Selecting a victim)**：最小化成本（Cost）。
* **回滾 (Rollback)**：將行程恢復到某個安全狀態並重啟 。
* **飢餓 (Starvation)**：需確保同一行程不會總是成為受害者（可將回滾次數計入成本因素）。

詳細請閱讀：[[deadlock-recovery | 死結恢復]]

---

# 參考資料
1. Operating System Concepts, 10/e