---
title: Advent of Code Day 7
publish: false
tags:
  - competitive-programming
  - advent-of-code
date: 2025-07-12
---
Part 1 很單純，但 Part 2 就需要動點腦了。
# Part 1
`std::span`，一個視圖。不擁有記憶體，只是指著別人的記憶體（像是 Go 或 Rust 的 Slice）。

```cpp
#include <span>

// 注意：這裡直接傳值 (pass by value) 即可，因為 span 很小（只有指標和長度）
int helper(int index, int row, std::span<std::string> fields) {
    // 這裡可以直接用 fields[0]，它指的就是切片後的第一個元素
    if (fields.empty()) return 0;

    // ... 你的邏輯
    return 0;
}
```

```cpp
// 第一次呼叫
helper(index, row, fields); // vector 會自動轉成 span

// 想要切片時，使用 subspan (這是 O(1) 操作，沒有複製)
helper(index, row, std::span(fields).subspan(1));
```

[Why can't I compile an unordered_map with a pair as key?](https://stackoverflow.com/questions/32685540/why-cant-i-compile-an-unordered-map-with-a-pair-as-key)
要自己做一個 PairHash 才可以。如何做一個 PairHash？

```cpp
struct PairHash {
	template <typename T>
	std::size_t
}
```

---
總用時：1hr, 30min