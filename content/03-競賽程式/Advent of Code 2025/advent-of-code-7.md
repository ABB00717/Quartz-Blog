---
title: Advent of Code Day 7
draft: true
tags:
  - competitive-programming
  - advent-of-code
date: 2025-07-12
---
# Part 1

遍歷整個 `fields`，如果上面有 `|` 就代表光束會射下來，如果這格是 `^` 就會需要分裂光束，也就是讓左右兩格也都變成 `|`。

```cpp
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> fields;
    int result = 0;

    // Read inputs into inputFile
    std::ifstream inputFile("input-day7");
    std::string line;
    while (std::getline(inputFile, line)) {
        fields.push_back(line);
    }

    for (char &ch : fields[0]) {
        if (ch == 'S') {
            ch = '|';
        }
    }

    // for (each row start from row2)
    for (int row = 1; row < fields.size(); row++) {
        for (int col = 0; col < fields[0].size(); col++) {
	        // if (up block is '|')
            if (fields[row - 1][col] == '|') {
                if (fields[row][col] != '^') {
                    fields[row][col] = '|';
                } else {
					// turn the left and right block to '|' if that
					// block is '.'
                    result++;
                    if (col != 0 && fields[row][col-1] != '^')
                        fields[row][col-1] = '|';
                    if (col != fields[0].size()-1 && fields[row][col+1] != '^')
                        fields[row][col+1] = '|';
                }
            }
        }
    }

    std::cout << result << std::endl;
}
```

# Part 2
就是現在這個分裂器（splitter），也就是這個光束產生的「光束宇宙」數量，是左右兩邊光束打下去後的光束宇宙數量加總。

```
int helper(index, row, fields: (from {i} to end)) {
    if (fields is NULL) {
        return 1;
    }

	if (under the index the block is '^')
		// helper to left
        sum += helper(index-1, row + 1, fields(from row+2 to end)) 
        // helper to right
        sum += helper(index+1, row + 1, fields(from row+2 to end)) 
    else
        return helper(index, row + 1, fields(from row+2 to end))
}
```

但這樣的時間複雜度會達到驚人的 $O(2^N)$！遞迴的威力，寶貝！因為它就是個完美的二元樹，遇到一個 `helper` 就會分裂，而假設每層都有一個 `helper`，那麼根據測資，數量就是 $2^{142}$！

但因為每次同樣 `index` 和 `row` 的結果都是一樣的，所以可以把結果紀錄起來，也就是可以用動態規劃。

> [!tip] 只要能寫成遞迴，而且結果不會根據狀態改變，就可以用動態規劃。

因為相當於每格最多計算一次，所以時間複雜度會變成簡單的 $O(R \times C)$。

```cpp
#include <fstream>
#include <iostream>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>
#include <span>

struct PairHash {
    template <class T1, class T2>
    std::size_t operator()(const std::pair<T1, T2>& p) const {
        auto h1 = std::hash<T1>{}(p.first);
        auto h2 = std::hash<T2>{}(p.second);
        return h1 ^ (h2 << 1); 
    }
};

#define DPTYPE std::unordered_map<std::pair<int, int>, long long, PairHash>

// int helper(index, row, dp, fields: (from {i} to end))
long long helper(int index, int row, DPTYPE& dp, std::vector<std::string>& fields) {
    if (row == fields.size()-1)
        return 1;

    if (dp.count({row, index}))
        return dp[{row, index}];

    int curRow = row+1;
    long long result = 0;
    if (fields[curRow][index] == '^') {
        if (index != 0)
            result += helper(index-1, curRow, dp, fields);
        if (index != fields[0].size()-1)
            result += helper(index+1, curRow, dp, fields);
    } else {
        return helper(index, curRow, dp, fields);
    }

    return dp[{row, index}] = result;
}

int main() {
    std::vector<std::string> fields;
    long long result = 0;

    // Read inputs into inputFile
    std::ifstream inputFile("input-day7");
    std::string line;
    while (std::getline(inputFile, line)) {
        fields.push_back(line);
    }

    DPTYPE dp;
    for (int i = 0; i < fields[0].size(); i++) {
        if (fields[0][i] == 'S') {
            result = helper(i, 0, dp, fields);
        }
    }

    std::cout << result << std::endl;
}
```

## 今天我學到的新東西
- [std::span](https://en.cppreference.com/w/cpp/container/span.html)
- [Why can't I compile an unordered_map with a pair as key?](https://stackoverflow.com/questions/32685540/why-cant-i-compile-an-unordered-map-with-a-pair-as-key)

---
總用時：1hr, 30min