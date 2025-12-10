---
title: Advent of Code Day 8
draft: false
tags:
  - advent-of-code
  - CP
date: 2025-12-08
---

> [!quote] 掌握不了[[自頂向下的智慧]]，差點放棄寫這題 ...

# Part 1

今天題目有點複雜，我向往常一樣從開始試著直接寫到結束，結果頻頻碰壁，寫了一小時硬是一點能跑得程式碼都沒有，只剩下腦中凌亂的想法和螢幕上雜亂的註解與義大利麵。

沈澱一下後，我決定不管任何資料結構、不管任何實作。假裝我想要的全部都有，直接把整個都寫出來。

```cpp
#include <algorithm>
#include <cmath>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#define EDGE_CALC(path, x, y, z) \
    path = std::sqrt(std::pow(x, 2) +\
                    std::pow(y, 2) +\
                    std::pow(z, 2))\

typedef struct {
    int x;
    int y;
    int z;
} Point;

int main() {
    std::ifstream inputFile("input-day8");
    std::string line;

    //  Store all points from inputFile
    std::vector<Point> points;
    while (std::getline(inputFile, line)) {
        std::stringstream ss(line);
        int x, y, z;
        ss >> x >> y >> z;
        points.push_back({x, y, z});
    }

    //  Calculate edge basted on point1 and point2
    float edge;
    vector<> edges;
    for (int i = 0; i < points.size(); i++) {
        for (int j = i+1; j < points.size(); j++) {
            float dx = points[i].x - points[j].x;
            float dy = points[i].y - points[j].y;
            float dz = points[i].z - points[j].z;
            EDGE_CALC(edge, dx, dy, dz);
            edges.push_back({edge, points[i], points[j]});
        }
    }
    //  Sort edges (std::less) (edge, point1, point2)
    std::sort(edges.begin(), edges.end(), [](const auto& a, const auto& b){
        return a.edge < b.edge;
    });

    //  Init Disjoint Set
    DS sets;
    //  Combine point1 and point2 in same disjoint set
    for (auto edge : edges) {
        Point point1 = edge.point1;
        Point point2 = edge.point2;

        sets[point1].combine(point2);
    }

    //  Find the 3 largest Disjoint Set
	vector<int> groupSize;
	//  Fill the groupSize
	for (int i = 0; i < points.size(); i++) {
		int root = sets.find(i);
		if (root is not recorded yet)
			groupSize.push_back(sets.getSize(root));
	}
    std::sort(groupSize.begin(), groupSize.end(), [](const auto& a, const auto& b){
        return a.size < b.size;
    });

    long long result = sets[0].size * sets[1].size * sets[2].size;
    std::cout << result;
}
```

我寫出來大概長這麼一陀，但思路看註解應該就蠻清楚的了。但還欠缺很多，最主要就是資料型別的定義。

`Edges` 要如何定義？`DS` 又要怎麼搞？還沒做，其實也都是小事啦，但我現在感覺超爽，跟剛剛[[headless-chicken|無頭蒼蠅]]的感覺真的完全不一樣了。

`DS` 就是 Disjoint Set，印象最深刻的就是它超級厲害的 `find`，時間複雜度是阿克曼函數。

總之寫出來長這樣
```cpp
#include <algorithm>
#include <cmath>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#define EDGE_CALC(path, x, y, z) \
    path = std::sqrt(std::pow(x, 2) +\
                    std::pow(y, 2) +\
                    std::pow(z, 2))\

typedef struct {
    int x;
    int y;
    int z;
} Point;

typedef struct {
    float weight;
    int u; // Index
    int v;
} Edge;

class DS {
public:
    std::vector<int> parent;
    std::vector<int> size;

    DS(int n) {
        parent.resize(n);
        size.resize(n, 1);
        for (int i = 0; i < n; i++) parent[i] = i;
    }

    int find(int i) {
        if (parent[i] == i) return i;
        return parent[i] = find(parent[i]);
    }

    void combine(int i, int j) {
        int root_i = find(i);
        int root_j = find(j);

        if (root_i != root_j) {
            parent[root_i] = root_j;
            size[root_j] += size[root_i];
        }
    }

    int getSize(int i) {
        return size[find(i)];
    }
};

int main() {
    std::ifstream inputFile("input-day8");
    std::string line;

    //  Store all points from inputFile
    std::vector<Point> points;
    while (std::getline(inputFile, line)) {
        std::stringstream ss(line);
        int x, y, z;
        char junk;
        ss >> x >> junk >> y >> junk >> z;
        points.push_back({x, y, z});
    }

    //  Calculate edge basted on point1 and point2
    float edge;
    std::vector<Edge> edges;
    for (int i = 0; i < points.size(); i++) {
        for (int j = i+1; j < points.size(); j++) {
            float dx = points[i].x - points[j].x;
            float dy = points[i].y - points[j].y;
            float dz = points[i].z - points[j].z;
            EDGE_CALC(edge, dx, dy, dz);
            edges.push_back({edge, i, j});
        }
    }
    //  Sort edges (std::less) (edge, point1, point2)
    std::sort(edges.begin(), edges.end(), [](const auto& a, const auto& b){
        return a.weight < b.weight;
    });

    int limit = 1000;
    if (edges.size() < limit) limit = edges.size();

    //  Init Disjoint Set
    DS sets(points.size());
    //  Combine point1 and point2 in same disjoint set
    for (int i = 0; i < limit; i++) {
        sets.combine(edges[i].u, edges[i].v);
    }

    //  Find the 3 largest Disjoint Set
    std::vector<int> groupSize;
    std::vector<bool> filled(points.size(), false);
    // Fill the groupSize
    for (int i = 0; i < points.size(); i++) {
        int root = sets.find(i);
        if (!filled[root]) {
            filled[root] = true;
            groupSize.push_back(sets.getSize(root));
        }
    }
    std::sort(groupSize.begin(), groupSize.end(), [](const auto& a, const auto& b){
        return a > b;
    });

    long long result = groupSize[0] * groupSize[1] * groupSize[2];
    std::cout << result;
}
```

# Part 2
就稍微改一下就好。最後 `root` 不相等的 `combine` 就是最後兩個併查集連起來的 `combine`。就是這樣。

```cpp
/*
...
*/

    bool combine(int i, int j) {
        int root_i = find(i);
        int root_j = find(j);

        if (root_i != root_j) {
            parent[root_i] = root_j;
            size[root_j] += size[root_i];

            return true;
        }

        return false;
    }
/*
...
*/

    //  Init Disjoint Set
    long long result;
    DS sets(points.size());
    //  Combine point1 and point2 in same disjoint set
    for (int i = 0; i < edges.size(); i++) {
        if (sets.combine(edges[i].u, edges[i].v))
            result = (long long)points[edges[i].u].x * points[edges[i].v].x;
    }

    std::cout << result;
}
```

明明 Leetcode 都刷了 500 題了，居然還會卡在這種題目這麼久 ...。看來真的是 Hard 刷太少了吧。不知道接下來幾天還會有怎樣的題目呢。