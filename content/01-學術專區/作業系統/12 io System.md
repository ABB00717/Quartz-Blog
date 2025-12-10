---
title: 12 I/O System
draft: true
tags:
  - operating-system
date: 2025-12-08
---

# 大綱
- I/O 的問題以及基礎
- I/O 的溝通方式
- I/O 的應用程式介面
- 內核如何與他們溝通
- 生命週期

---
Polling 要一直循環等會浪費超多資源。中斷其實也是。

- 速度差
- 裝置有太多種類

裝置需要驅動作為中間的溝通橋樑。
- DMA（Direct Memory Access）
- MMIO（Memory-mapped I/O）
- 控制器（Controller）

# 應用程式介面

## 存取方式
- Blocking
- Nonblocking
- Asynchronous

Vectored I/O 讓內核可以透過一個系統呼叫就能同時操作不同 I/O 裝置。

[[CS:APP: System-Level I/O]]


# 內核
## 緩衝區（Buffer）
快取和緩衝區（Buffer）不同。快取是把較低記憶體階層的值複製到它這裡，藉此提昇存取速度。但緩衝區是是提供一個空間緩衝兩個裝置間速度的差異，像是 I/O 的資料傳送速度慢 CPU 的超多倍，所以讓那些 I/O 慢慢先把那些資料都放進緩衝，都放好組裝好以後再請 CPU 來存取。

## 排存（Spooling）
印表機

# 生命週期
==這個圖很重要==

內核存取 I/O。如果在內核快取內若能找到資料就直接用，反之則和裝置驅動請求資料。裝置就會把內核的指令轉換成裝置控制器看得懂的指令。把資料都放進緩衝區以後，就發出中斷請內核來查看，然後就重新執行該指令

![[Interrupt Handling Control Flow.png]]