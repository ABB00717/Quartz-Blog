---
title: 03 Transport Layer
draft: true
tags:
  - computer-networks
date: 2025-12-10
---

# 大綱
- UDP
- TCP
	- 如何透過可能遺失的通道進行可靠通訊
	- 如何實現上述原理
- 網路擁塞
	- 成因與後果
	- 控制

segment -> 段 (TCP, UDP 封包的統稱)
datagram -> 資料包（專指網路層封包）

# 多工與解多工
將主機到主機的傳遞擴展為行程到行程的傳遞，稱為傳輸層多工和解多工。

每個行程都有自己的一到多個通訊端。接收端會檢查欄位，並把這段導向正確的通訊端，這稱為解多工。而為資料區塊封裝標頭、建立分段、並且分段傳送的過程則稱為多工。

- 通訊端必須有特殊識別碼
- 每個段都必須標明要傳到哪個通訊端，就是 Source Port 和 Dest. Port

有些 Port（1~1023）會保留給特殊用途
# UDP
除了多工與解多工，幾乎沒有做其他事情。
%%我只知道他不在乎你有沒有收到%%
![[image-6.png]]

> 雖然UDP具備錯誤檢查功能，但不會主動處理錯誤。部分UDP實作會直接丟棄損壞的段，也有些實作會將損壞段連同警告一併傳遞給應用層。

# 可靠資料傳輸原理

可靠通道：傳輸的資料不會 corrupt 或遺失，且所有資料會按照順序送達。

基本假設是：封包將按照傳送順序遞送，但部分封包可能遺失；也就是說，底層通道不會重新排序封包。

## rdt
## 回退 N 步（GBN）
## 選擇性重複（SR）

一個 buffer 選擇傳送封包的範圍
一直傳直到末尾，如果有收到第一個封包的 ACK，則就把 buffer 往右移，否則就重傳第一個封包。

[A Mathematical Theory of Communication](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf)：一個保證能做到可靠傳輸的方法
# TCP
連線導向，因為在開始傳送資料以前，兩個行程必須先交握。

- 會切割成 MSS 的資料區塊

![[image-7.png]]
較重要的有 Sequence Number 和 Ack. Number

# 網路壅塞控制的原則

# TCP 網路流量控制