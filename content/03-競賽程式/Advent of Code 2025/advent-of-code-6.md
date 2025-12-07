---
title: Advent of Code Day 6
publish: true
tags:
  - advent-of-code
  - competitive-programming
date: 2025-12-06
---

# Part 1 
挺單純的，大致流程如下：

```
填滿 `numbers` 的陣列
並且紀錄每個 column 對應的運算子
遍歷每個 column 針對不同運算子作不同操作並求最終值
把每個 column 的最終值加起來
```

寫成程式碼就是

```cpp
#include <cctype>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
int main() {
    std::ifstream inputFile("input-day6");

    std::string line;
    std::vector<std::vector<int>> numbers;
    std::vector<char> operators;
    while (std::getline(inputFile, line)) {
        int number;
        char oper;
        std::vector<int> line_numbers;

        // Read numbers in line
        if (std::isdigit(line[0])) {
            std::stringstream ss(line);
            while (ss >> number) {
                line_numbers.push_back(number);
            }

            numbers.push_back(line_numbers);
        } else {
            // Read operators in line
            std::stringstream ss(line);
            while (ss >> oper) {
                operators.push_back(oper);
            }
        }
    }

    int n = operators.size();
    long long result = 0;
    // Performing operations;
    for (int i = 0; i < n; i++) {
        long long temp = numbers[0][i];
        for (int row = 1; row < numbers.size(); row++) {
            switch (operators[i]) {
                case '+':
                    temp += numbers[row][i];
                    break;
                case '*':
                    temp *= numbers[row][i];
                    break;
            }
        }

        result += temp;
    }

    std::cout << result << std::endl;
}
```

# Part 2
幾乎要把上面的程式碼重寫。

```
result = 0
for ch : 從右到左一個一個字元讀取
	cur_number : 由上到下組合起來
	if 最後一個是運算子
		result = 針對不同運算子操作，算出最終值
```

寫成程式碼就是

```cpp
#include <cctype>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
int main() {
    std::ifstream inputFile("input-day6");

    std::string line;
    std::vector<std::string> inputLines;
    while (std::getline(inputFile, line)) {
        inputLines.push_back(line);
    }

    int lineSize = inputLines[0].size();
    int inputSize = inputLines.size();
    std::vector<long long> cur_line_numbers;
    long long result = 0;
    for (int col = lineSize-1; col >= 0; col--) {
        char dig = ' ';

        long long cur_number = 0;
        for (int row = 0; row < inputLines.size(); row++) {
            if (isdigit(inputLines[row][col])) {
                cur_number *= 10;
                cur_number += inputLines[row][col] - '0';
            }
        }

        if (cur_number != 0)
            cur_line_numbers.push_back(cur_number);

        if (inputLines[inputSize-1][col] != ' ') {
            char oper = inputLines[inputSize-1][col];
            long long temp = cur_line_numbers[0];
            switch (oper) {
                case '+':
                    for (int i = 1; i < cur_line_numbers.size(); i++) {
                        temp += cur_line_numbers[i];
                    }
                    break;
                case '*':
                    for (int i = 1; i < cur_line_numbers.size(); i++) {
                        temp *= cur_line_numbers[i];
                    }
                    break;
                default:
                    std::cout << "Unknown Operations!\n";
                    exit(-1);
            }

            result += temp;
            cur_line_numbers.clear();
            std::cout << result << std::endl;
        }
    }

    std::cout << result << std::endl;
}
```