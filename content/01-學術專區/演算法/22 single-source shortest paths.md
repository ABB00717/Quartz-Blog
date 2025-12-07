---
title: 22 Single-Source Shortest Paths
draft: false
tags:
  - algorithm
  - graph-algorithm
date: 2025-06-12
---
演算法最重要的就是定義好輸入和輸出。對於單向最短路徑演算法（SSSP），我們只有幾個關鍵的屬性：
- 圖：$G = (V,E)$，和一個起點 $s \in V$
- 邊：每條邊 $(u, v)$ 都有一個權重 $w(u, v)$
- 目標：找出從 $s$ 到圖中每一個頂點 $v$ 的最短路徑權重 $\delta(s, v)$

> [!important] 最佳子結構
> 如果 $s \rightarrow \dots \rightarrow u \rightarrow v$ 是 $s \rightarrow v$ 的最短路徑，那麼 $s \rightarrow \dots \rightarrow u$ 也一定會是 $s \rightarrow u$ 的最短路徑。所以我們可以用貪婪演算法和動態規劃來解決這種問題。

> [!danger] 負無限權重
> 如果圖裡有負無限權重的邊，那最短路徑就是未定義的（$-\infty$）。而負環則是另一種負無限權重，因為你理論上可以一直刷那個環來減少路徑權重 $\delta$。
# 大綱
- 核心操作
	- 鬆弛
- 演算法分類
	- 無權重
	- 權重非負
	- 有向無環圖：Dijkstra
	- 含負權重、但無負環（不然就是無限未定義了）：Bellman-Ford

# 核心操作
有些核心的概念，是不論什麼種類的 SSSP 都會用到的核心概念。
## 鬆弛
剛開始先將所有點的距離 $d[v]$ 設定成 $\infty$，只有起點 $d[s] = 0$。

如果能找到更好的，再慢慢縮小。

---
## Dijkstra 演算法
既然我們最短路徑遵守最佳子結構，那假設我們前面的路徑權重是遞增的話，那是不是每一次只要選擇當前可用的最小 $d(v)$ 節點並用它做 BFS 就可以了呢？

因為這過程是一層一層慢慢往上，所以也被稱為迭代式演算法，亦即第 $k$ 次迭代後可以得知 $k$ 個目的地節點的最低成本路徑。

- `d(v)`：來源節點到目的地 `v` 的最低成本路徑
- `p(v)`：來源節點到 `v` 的當前最低成本路徑中 `v` 的前一個節點

```c
// start from s
void Dijkstra(Graph G, Vertex s) {
	// Init
	for (each vertex v in G) {
		d[v] = INF;
		p[v] = NULL;
	}
	d[s] = 0
	
	// Contains all vertex in G
	PriorityQueue Q = BuildQueue(G);
	
	// 因為迭代式演算法的特性，所以剛好計算 G.size() 次就可以
	// 把所有點的最短路徑算出來
	// O(E)
	while (!Q.empty()) {
		vertex u = ExtractMin(Q); // Vlog(V)
		
		for (each neighbor v of u) {
			int weight = GetWeight(u, v);
			
			// 鬆弛
			if (d[v] > d[u] + weight) {
				d[v] = d[u] + weight;
				p[v] = u;

				// Update the priority order in Q
				DecreaseKey(Q, v, d[v]);
			}
		}
	}
}
```

### 時間複雜度
$$
O(\text{遍歷所有的邊 + Binary Heap 的 ExtractMin}) \rightarrow O(E + V \log{V})
$$
## Bellman-Ford
但 Dijkstra 的問題在於，它假設路徑的成本只會遞增，所以不能處理權重為負的情況。

Bellman 那時的想法是：「如果我知道怎麼走到終點 $v$，那我的最後一步是從哪裡得來的？」這就是最佳子結構的逆向思考。將上述思考換成數學就是
$$
d[v] = \min(d[u] + w(u, v))
$$
後來這條公式被稱為貝爾曼方程式（Bellman Equation）。

可問題是，要知道 $d[v]$ 需要知道 $d[u]$，所以可能需要知道 $d[k]$，但 $d[k]$ 又可能回頭依賴 $d[v]$。遇到這種循環依賴，該如何是好？ 所以我們要限縮問題，不該一上來就直接問結果，要循序漸進。**如果我限制「走的步數」呢？** 既然直接問最短路徑會造成無窮迴圈，那我改成問：
1. 走 1 步能到的最短路徑是多少？（這很簡單，就是起點連出去的邊）
2. 走 2 步能到的最短路徑是多少？（基於走 1 步的結果來算）
3. 走 $k$ 步能到的最短路徑是多少？

我們知道要構成有 $V$ 個頂點的連通圖最少要有 $V-1$ 條邊，也就是說最多 $k = V-1$ 輪就必定可以知道結果！
### 負環檢測
然而有個討厭例外，就是負環。我們說過，如果有負環就可以無限鬆弛下去，所以如果跑了 $V-1$ 次還可以繼續鬆弛，那就代表一定有負環。

```c
bool BellmanFord(Graph G, Vertex s, int V, Edge edges[]) {
	// Init
    for (each vertex v in G) {
        d[v] = INF;
        p[v] = NULL;
    }
    d[s] = 0;

	// At most repeat V-1 times
    for (int i = 1; i <= V - 1; i++) {
        bool relaxed_in_this_round = false; 

        // Iterate all edges (the order doesn't matter)
        for (each edge (u, v) in edges) {
            int weight = GetWeight(u, v);

			// Relax
            if (d[u] != INF && d[v] > d[u] + weight) {
                d[v] = d[u] + weight;
                p[v] = u;
                relaxed_in_this_round = true; 
            }
        }
        
		// Early Termination
        if (!relaxed_in_this_round) {
			// If there's a negative cycle, then
			// we could definitly continue to converge, but it
			// ended, so there's no negative cycle
            return true;
        }
    }

	// Negative Cycle Detection
    for (each edge (u, v) in edges) {
        int weight = GetWeight(u, v);
        if (d[u] != INF && d[v] > d[u] + weight) {
			// There's a negative cycle!
            return false; 
        }
    }

    return true;
}
```
### 時間複雜度
$$
O(\text{遍歷 V-1 次} \cdot \text{遍歷所有的 E}) \rightarrow O(V \cdot E)
$$