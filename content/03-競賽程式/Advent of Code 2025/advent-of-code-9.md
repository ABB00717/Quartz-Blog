---
title: Advent of Code Day 9
draft: false
tags:
  - advent-of-code
  - CP
date: 2025-12-08
---

嘗試使用[[literate-programming]]的方法來解決這道競賽題

# Part 1
... 結果我直接寫出來了

# Part 2
![[image-5.png]]
我猜我們要找所有能連成一條線的點 `pairs`，然後把那些 `pair` 全部框在一起，把所有可行的結果都計算一遍後選出最大的。

```
#define PointPair 

vector<PointPair> linePairs: 建構所有直線的 `pairs`
vector<vector<PointPair>> possibleRect: 所有可以圈起來形成封閉 rectangle 的直線集合

// 建構 linePairs
for (each redBlock in redBlocks) {
	for (each anotherRedBlock in (red blocks after redBlock)) {
		if (redBlock 和 anotherRedBlock 的 x 或 y 座標是一樣的)
			把 red, another 放入 linePairs 後面
	}
}

// 建構 possibleRect
for (each linePair in linePairs) {
	vector<PointPair> tempRect: 由目前 linePair 出發可構成的 rectangle
	// 但是該用什麼方法建構這個 tempRect？
}

long result = 0;
計算所有 possibleRect 的 rectangle 面積，並取最大的放進 result
```

好吧，我接下來完全沒有頭緒。