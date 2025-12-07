---
title: Obsidian 無痛轉成 Blog
publish: true
tags:
  - obsidian
  - blog
date: 2025-12-06
---

原本我都是用 Jekyll，但有的格式和 Obsidian 無法相容（連最基礎的 KaTeX 都沒辦法！），所以只好找新的方案。很幸運找到這個叫做 [Quartz](https://quartz.jzhao.xyz/) 的開源專案可以完全支援 Obsidian 的 Markdown 風格！

> 這專案還是由 Obsidian 官方贊助的， 盡管他們自己有功能的官方付費方案 。

剛點進去就有安裝步驟，照著安裝就好了。你可以看它在本地端的樣子
```shell
npx quartz build --serve
```

> [!warning] 記得 `content` 內要有 index 檔案！

建議先新增一個 Template。

```
---
title: Example Title
draft: false
tags:
  - example-tag
---
```

有興趣可以[參考官網](https://quartz.jzhao.xyz/)看更詳細的教學。
> 1. [Writing content](https://quartz.jzhao.xyz/authoring-content) in Quartz
> 2. [Configure](https://quartz.jzhao.xyz/configuration) Quartz’s behaviour
> 3. Change Quartz’s [layout](https://quartz.jzhao.xyz/layout)
> 4. [Build and preview](https://quartz.jzhao.xyz/build) Quartz
> 5. Sync your changes with [GitHub](https://quartz.jzhao.xyz/setting-up-your-GitHub-repository)
> 6. [Host](https://quartz.jzhao.xyz/hosting) Quartz online

# 常用指令
```shell
npx quartz sync # Push changes to remote repo
```

# 直接與 Obsidian 連接
作者也有為 Obsidian 做[專屬外掛](https://github.com/saberzero1/quartz-syncer)，可以單純在 Obsidian 內做一切需要的操作。

[外掛文檔](https://saberzero1.github.io/quartz-syncer-docs/)

---
# 參考資料
1. https://www.youtube.com/watch?v=6s6DT1yN4dw