---
title: 資安資源酸辣湯
draft: false
tags:
  - cyber-security
date: 2025-12-10
---

「我要精通資訊安全」這句話和「我要精通資訊工程」差不多含糊，但偏偏與資訊工程相比，資訊安全的地圖真他媽亂，亂到靠北（至少在我外行眼裡）。

於是我就在想，乾脆先不要試著釐清到底哪些東西該在哪裡分類、整個領域的架構在哪裡。不如我就看到什麼「感覺和資訊安全有關的東西」就全丟進這個酸辣湯裡頭，之後看能不能理出個什麼來。

> [!note] 挫敗感
> 我還記得大一下時我就有嘗試踏入資安，那時借的第一本書叫做 [C++ 黑客編程揭秘與防範, 3/e](https://www.tenlong.com.tw/products/9787115493729)。齁齁，幹，看三頁就放棄了，你媽逼，根本看不懂。至於內容是什麼根本忘記了，因為在我眼裡根本就是天書、亂碼，就像你不會記得存在本地端裡 OpenSSH 存的私鑰長什麼樣子。
>
> 所以書籍還是要慎選，不要一次跳太多級，不然你還沒開始就會直接放棄。雖然如此，也請不要妄自菲薄，[你欠缺的只是先備知識](https://lelouch.dev/blog/you-are-probably-not-dumb/)！

> [!note] 我的啟蒙教材
> 大二下後的暑假讀了 [CS:APP](https://csapp.cs.cmu.edu/)，其中的 [Bomb Lab 以及 Buffer Lab](https://csapp.cs.cmu.edu/3e/labs.html) 就是我的啟蒙教材。一個教你基礎逆向工程，最後要你看懂用組合語言寫的鏈結串列排序程式。另一個是要你利用緩衝區溢位（Buffer Overflow）以及 Gadget 修改堆疊（Stack）內的回傳地址。
>
> 雖然資安並不是這本書的重點，但相比起後面的自幹指令集還有各種系統程式設計，這真的是我最喜歡的作業。藉此又燃起我對資安的興趣。


[Cyber Security Expert Roadmap](https://roadmap.sh/cyber-security)

至於我資安的最終目標，因為我有個同學在高中時就拿到 OSCP，也因此這順理成章的也成為我的目標。（可是真的好貴啊 @@）

- Linux 基礎命令行工具
- 組合語言基本語法與開發

---

# 資源
以下丟一些我找到的資源

## 部落格
- [b3rm1nG](https://medium.com/@b3rm1nG)
	- [如何成為一名駭客](https://medium.com/@b3rm1nG/%E5%A6%82%E4%BD%95%E6%88%90%E7%82%BA%E4%B8%80%E5%90%8D%E9%A7%AD%E5%AE%A2-a298082f3c6a)
- [Cymetrics Tech Blog](https://tech-blog.cymetrics.io/)
	- [Crystal](https://tech-blog.cymetrics.io/posts/crystal/)
- [HackerCat 駭客貓咪](https://hackercat.org/)
- [0xdf Hacks Stuff](https://0xdf.gitlab.io/)
  > 不得不介紹，它的許多 HTB 的 Writeup 都寫的極好，有興趣可以看看。 
- [Orange Tsai](https://blog.orange.tw/)
- [123ojp 的資安簡報](https://hackmd.io/@foxo-tw/slides/https%3A%2F%2Fslides.foxo.tw%2F)
- [PT Note 滲透測試重新打底](https://pt-note.coderbridge.io/page/3/)

## 練習網站
- [pwn.college](https://pwn.college/)
- [PortSwigger](https://portswigger.net/web-security/all-labs)

## 書本
- [揭秘家用路由器 0day 漏洞挖掘技術](https://www.tenlong.com.tw/products/9789863478805)
- [Hacking: The Art of Exploitation, 2nd Edition](https://learning.oreilly.com/library/view/hacking-the-art/9781593271442/)
- [The Hardware Hacking Handbook](https://learning.oreilly.com/library/view/the-hardware-hacking/9781098129835/)

## 活動
- [HITCON](https://hackmd.io/@foxo-tw/slides/https%3A%2F%2Fslides.foxo.tw%2F)