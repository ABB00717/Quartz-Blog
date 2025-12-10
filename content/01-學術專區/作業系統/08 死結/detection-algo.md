---
title: 死結檢測
draft: false
tags:
  - operating-system
  - deadlock
date: 2025-12-10
---
若系統不採用死結預防（Prevention）或死結避免（Avoidance）演算法，則死結可能發生 。在此情況下，系統必須提供：
1.  **檢測演算法 (Detection Algorithm)**：用於檢查系統狀態以判定是否已發生死結 。
2.  **恢復機制 (Recovery Scheme)**：用於從死結狀態中恢復 。

死結檢測演算法依據資源類型的實例數量（Single vs. Multiple Instances）而有不同的實作方式。

## 單一實例資源 (Single Instance of Each Resource Type)

若系統中每種資源類型只有一個實例，死結檢測可透過**等待圖 (Wait-for Graph)** 進行 。

![[image-13.png]]

### 等待圖結構
等待圖是資源分配圖（Resource-Allocation Graph）的變形：
* **節點**：僅包含行程（Processes），移除了資源節點。
* **邊**：$P_i \rightarrow P_j$ 表示行程 $P_i$ 正在等待 $P_j$ 所持有的資源 。

### 檢測邏輯
* 系統需週期性地執行演算法，在等待圖中搜尋是否存在**循環 (Cycle)**。
* 若圖中存在循環，則代表系統已發生死結 。
* **複雜度**：若圖中有 $n$ 個頂點，檢測循環的演算法複雜度約為 $O(n^2)$ 。



## 多重實例資源 (Multiple Instances of a Resource Type)

當資源類型擁有多個實例時，等待圖無法有效運作，需改用類似銀行家演算法的檢測演算法 。

### 資料結構
設系統中有 $n$ 個行程與 $m$ 種資源類型：
* **Available**：長度為 $m$ 的向量，表示目前各資源類型的可用數量 。
* **Allocation**：$n \times m$ 矩陣，表示各行程目前已持有的資源數量 。
* **Request**：$n \times m$ 矩陣，表示各行程**當前正在請求**的資源數量。若 `Request[i][j] == k`，表示 $P_i$ 正在請求 $k$ 個 $R_j$ 。

> [!warning] 與銀行演算法的差異
> 與銀行家演算法不同，這裡使用的是 `Request`（當前確定的請求）而非 `Need`（未來最大潛在需求 Max - Alloc）。

### 檢測演算法 (The Algorithm)

此演算法用於判斷當前系統狀態下的行程是否處於死結。

1.  **初始化 (Initialization)** ：
    * 令 `Work` 為長度 $m$ 的向量，初始化為 `Work = Available`。
    * 令 `Finish` 為長度 $n$ 的向量。
    * 對於每個行程 $i$：
        * 若 `Allocation[i] != 0`（持有資源），則 `Finish[i] = false`。
        * 若 `Allocation[i] == 0`（未持有資源），則 `Finish[i] = true`（該行程不會造成死結，視為可完成）。

> [!question] `Allocation[i] == 0` 也可能卡死
> 若 `Allocation[i] == 0`，但它 `Request[i]` 還是無法被滿足。這時應該叫做系統資源不足或是飢餓，而不是死結。因為它沒有滿足持有並等待以及循環等待的條件。因此在這裡直接標示 `Finish[i] = true`，因為它不會造成死結。

2.  **尋找可滿足行程 (Find Process)** ：
    * 尋找一個索引 $i$ 滿足：
        * `Finish[i] == false`
        * `Request_i <= Work`
    * 若找不到這樣的 $i$，跳至步驟 4。

3.  **回收資源 (Reclaim Resources)** ：
    * 假設該行程能獲得資源並完成執行，釋放資源：
        * `Work = Work + Allocation_i`
        * `Finish[i] = true`
    * 跳回步驟 2。

4.  **結論 (Conclusion)** ：
    * 若存在某個索引 $i$ 使得 `Finish[i] == false`，則系統處於死結狀態。
    * 所有 `Finish[i] == false` 的行程 $P_i$ 即為死結行程。

### 實例推演

考慮系統狀態 ($T_0$)，有 5 個行程 ($P_0 \sim P_4$) 與 3 種資源 (A, B, C) ：

| 行程 | Allocation | Request | Available |
| :--- | :--- | :--- | :--- |
| **$P_0$** | 0 1 0 | 0 0 0 | **0 0 0** |
| **$P_1$** | 2 0 0 | 2 0 2 | |
| **$P_2$** | 3 0 3 | 0 0 0 | |
| **$P_3$** | 2 1 1 | 1 0 0 | |
| **$P_4$** | 0 0 2 | 0 0 2 | |

**推演過程**：
1.  **初始化**：
    * `Work = (0, 0, 0)`。
    * 所有行程 `Allocation` 皆不為 0，故 `Finish` 全為 `false`。
2.  **第一輪**：
    * $P_0$ 的 `Request` (0,0,0) $\le$ `Work` (0,0,0)。
    * $P_0$ 完成，釋放資源：`Work` = (0,0,0) + (0,1,0) = **(0,1,0)**。`Finish[0] = true`。
3.  **第二輪**：
    * $P_2$ 的 `Request` (0,0,0) $\le$ `Work` (0,1,0)。
    * $P_2$ 完成，釋放資源：`Work` = (0,1,0) + (3,0,3) = **(3,1,3)**。`Finish[2] = true`。
4.  **後續**：
    * 依序檢查，$P_3$ (1,0,0)、$P_1$ (2,0,2)、$P_4$ (0,0,2) 的請求皆小於 `Work`。
    * 所有 `Finish` 最終皆為 `true`。
5.  **結果**：無死結 。

> **死結案例**：若 $P_2$ 多請求一個 C，即 `Request_2 = (0,0,1)`，則推演至 $P_0$ 完成後 `Work=(0,1,0)`，無任何行程請求可被滿足，系統陷入死結（涉及 $P_1, P_2, P_3, P_4$）。

## 檢測時機 (Detection-Algorithm Usage)

檢測演算法的執行頻率取決於兩個因素 ：
1.  **死結發生的頻率**：若死結經常發生，應頻繁檢測。
2.  **死結發生後的影響範圍**：若死結持續過久，涉及死結的行程數量會增加（級聯效應），導致恢復成本提高。

**建議策略**：
* **低資源利用率觸發**：例如當 CPU 利用率低於 40% 時，這通常意味著許多行程處於阻塞等待狀態，可能有死結發生 。
* **定時觸發**：例如每小時執行一次。