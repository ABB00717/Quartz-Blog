---
title: 13 File-System Interface
draft: true
tags:
  - operating-system
date: 2025-12-08
---

如何把不同目錄、檔案的位址與硬體磁區內的區塊對應在一起？對於使用者而言，檔案應該是連續的，但事實上在硬碟裡面是怎麼存的我們並不知道。

> 這是整本書裡最廢的一章
> 
> \- 鄭欣明

# 大綱
- 檔案的概念
- 存取檔案
- 目錄的架構
- 掛載檔案系統
- 檔案共享
- 保護

# 檔案的概念
- 特性
- 操作：讀寫等等

# 存取檔案
Open Files
- Open-file table
- File-open count

![[Open-File Table.png | Open-File Table]]

> CS:APP 裡面有講！！

## 目錄
- General Graph Directory

> 差別：要不要允許迴圈？

# 檔案系統的架構
這些檔案系統相關的架構，是會存在硬碟內的。如果每次要讀都要從硬碟查關聯，那速度超慢啊！

和 PCB 一樣，檔案也有 FCB（File Control Block）。儲存權限、大小之類的抽象東西

Layered File System
I/O statement -> Logical File System -> File-Organization Module -> Basic File System -> I/O Control -> Devices

> 對於使用者而言是從檔案出發，所以那些檔案如何對應到那些 Block，就是上圖的流程

- File System Layer
總之就是硬碟區塊與檔案之間的轉換

Basic file System ：給底層看得懂的命令
File Organization Module：除存硬碟區塊

除了 FCB，還有 BCB（Boot Control Block）和 VCB（Volume Control Block）。

- Virtual File System
file-system interface -> VFS -> Logical File System

## Contiguous Allocation
真的儲存在連續的實體硬碟區塊。
start, size
會有斷裂的問題（和記憶體一樣的問題）
## Linked Allocation
start, end 都直接儲存區塊的位址
FAT（File Allocation Table）就是這麼存的
## Indexed Allocation

### Unix I-node
裡面存元檔案（Metadata）紀錄每個區塊裡面是什麼資料。
Grouping and Counting

> VFS 和 NFS 看一看