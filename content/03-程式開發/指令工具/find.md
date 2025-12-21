---
title: find
tags:
  - "#command-line-tool"
date: 2025-06-12
---
# 參數
常用的有：
- `--maxdepth`
- `-path`
- `-prune`
- `-exec`

詳細請參考 [man find](https://man7.org/linux/man-pages/man1/find.1.html)
# 範例

搜尋除了 `node_modules` 資料夾以外的所有檔案，並印出檔案內有 "Welcome to Quartz" 的檔案名稱。
```shell
$ find ./ -path "*/node_modules/*" -prune -o -type f -exec grep -H "Welcome to Quartz" {} \;
# ...
```