---
title: find
draft: true
tags:
  - "#command-line-tool"
date: 2025-06-12
---
# Args
- -path {pattern}:
    指定路徑的匹配模式。支援萬用字元（如 *）。
    - 例如：`"*/node_modules/*"` 表示匹配任何路徑中包含 `node_modules` 的資料夾。
- -prune:
    "修剪"（Prune）。告訴 find 不要進入當前匹配到的目錄。
    - 通常與 `-path` 配合使用，用來排除特定資料夾。
- -o:
    邏輯 "OR"（或者）。這是排除語法的關鍵。
    - 邏輯是：`如果路徑匹配且被 Prune (左邊成立) -> 停下` **OR** `(左邊不成立) -> 繼續執行後面的搜尋 (右邊)`。
- -type:
    指定搜尋的類型。
    - `f`: 檔案 (File)
    - `d`: 目錄 (Directory)
- -exec ... \;:
    對找到的每一個檔案執行後面的命令。
    - `{}`: 代表找到的檔案路徑。
    - `\;`: 代表 exec 命令的結束（必須轉義）。
    - **變體**: `-exec ... +` (將多個檔案打包成一行指令執行，速度較快)。
# 範例

搜尋除了 `node_modules` 資料夾以外的所有檔案，並印出檔案內有 "Welcome to Quartz" 的檔案名稱。
```shell
$ find ./ -path "*/node_modules/*" -prune -o -type f -exec grep -H "Welcome to Quartz" {} \;
./docs/index.md:title: Welcome to Quartz 4
./content/02-程式開發/指令工具/find.md:搜尋除了 `node_modules` 資料夾以外的所有檔案，並印出檔案內有 "Welcome to Quartz" 的檔案名稱。
./content/02-程式開發/指令工具/find.md:find ./ -path "*/node_modules/*" -prune -o -type f -exec grep -H "Welcome to Quartz" {} \;
# ...
```