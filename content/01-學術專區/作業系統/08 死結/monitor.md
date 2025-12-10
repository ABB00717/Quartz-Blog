---
title: 監視器（Monitor）
draft: false
tags:
  - operating-system
date: 2025-12-10
---
**監視器**（英語：Monitor），是一種高階的行程同步機制（Process Synchronization Mechanism）。它被定義為一種抽象資料型別（Abstract Data Type, ADT），用於封裝共享資源及其操作，以確保在多執行緒或多行程環境下的安全性。

與號誌（Semaphore）相比，監視器提供了更易於管理和更不易出錯的同步模型。其核心特性在於**自動的互斥存取**（Automatic Mutual Exclusion）：同一時間，只允許一個行程（或執行緒）在監視器內部執行任何程序。

-----

## 1\. 歷史背景

監視器的概念最早由 **C.A.R. Hoare** 與 **Per Brinch Hansen** 於 1970 年代初期提出。其設計初衷是為了解決號誌（Semaphore）在使用上過於分散、易導致死結（Deadlock）或競態條件（Race Condition）且難以偵錯的問題。

監視器的設計將同步控制的責任從「程式設計師必須手動撰寫 P/V 操作」轉移到了「編譯器或程式語言的執行環境」上。現代語言如 Java 的 `synchronized` 關鍵字、C\# 的 `Monitor` 類別，皆為此概念的實作。

-----

## 2\. 架構與組成

從結構上看，監視器類似於物件導向程式設計中的「類別（Class）」，它包含以下三個主要部分：

1.  **共享變數（Shared Variables）**：

      * 這是監視器所保護的資料。
      * 這些變數是**私有的（Private）**，僅能透過監視器內部定義的程序（Procedures）進行存取，外部行程無法直接讀寫。

2.  **程序（Procedures / Methods）**：

      * 這是一組定義在監視器內部的函式。
      * 外部行程若想存取共享變數，必須呼叫這些程序。
      * **互斥保證**：監視器確保任何時候，只有一個行程能處於這些程序之中。若有一個行程正在執行監視器內的程序，其他試圖呼叫程序的行程將被阻塞（Blocked），並在監視器外部的入口佇列（Entry Queue）中等待。

3.  **條件變數（Condition Variables）**：

      * 雖然監視器保證了互斥，但行程有時需要等待特定條件成立（例如：緩衝區非空）。
      * 條件變數提供了 `Wait` 和 `Signal` 操作，用於管理在監視器內部等待資源的行程。

-----

## 3\. 同步機制

監視器的運作依賴於兩個層次的同步：**互斥（Mutual Exclusion）** 與 **條件同步（Condition Synchronization）**。

### 3.1 互斥 (Mutual Exclusion)

這是監視器最基本的特性。當一個行程呼叫監視器的程序時：

  * 若監視器內無其他行程執行，該行程獲得鎖定（Lock）並進入執行。
  * 若監視器內已有行程正在執行，呼叫者會被暫停，並放入**入口佇列（Entry Queue）**。

### 3.2 條件變數與操作

僅有互斥是不夠的，行程可能在進入監視器後發現無法繼續執行（例如：資源不足）。此時需要**條件變數**（通常宣告為 `condition x, y;`）。

針對條件變數 `x`，主要有兩個操作：

1.  **`x.wait()`**：

      * 執行此操作的行程會釋放監視器的互斥鎖（Monitor Lock）。
      * 該行程進入屬於變數 `x` 的\*\*條件佇列（Condition Queue）\*\*中等待。
      * 這讓其他行程有機會進入監視器執行，從而可能改變狀態以滿足 `x` 的條件。

2.  **`x.signal()`**（或稱 notify）：

      * 喚醒一個正在 `x` 條件佇列中等待的行程。
      * 若沒有行程在等待，則此操作無效（與號誌不同，號誌會累計數值，監視器的 Signal 則是無記憶的）。

-----

## 4\. 信號語意 (Signaling Semantics)

當一個行程 P 執行了 `x.signal()` 喚醒了行程 Q 後，監視器內就會有兩個活躍的行程（P 和 Q）。為了維持「同一時間只有一個行程執行」的原則，必須決定誰優先執行。這衍生出了兩種主要的語意模型：

### 4.1 Hoare 語意 (Signal-and-Wait)

  * **機制**：當 P 執行 Signal 喚醒 Q 時，P **立即暫停**並交出監視器控制權，讓 Q 馬上執行。等到 Q 離開或等待時，P 才恢復執行。
  * **優點**：邏輯證明較容易。Q 被喚醒時，條件必然為真（因為 P 剛做完改變就切換給 Q）。
  * **缺點**：上下文切換（Context Switch）次數較多，實作成本高。

### 4.2 Mesa 語意 (Signal-and-Continue)

  * **機制**：當 P 執行 Signal 喚醒 Q 時，P **繼續執行**直到完成或自行等待。Q 僅是被從等待佇列移到就緒佇列（Ready Queue），等待 P 離開監視器後才有機會搶奪鎖定。
  * **優點**：減少了上下文切換，效率較高，是現代作業系統和語言（如 Java, POSIX Threads）的主流實作。
  * **注意**：因為 Q 被喚醒到實際執行之間有時間差，條件可能被其他插入的行程改變。因此，檢查條件必須使用 `while` 迴圈而非 `if`。

> **程式碼慣例（Mesa 語意）：**
>
> ```c
> while (!condition) {
>     x.wait();
> }
> // 執行資源操作
> ```

-----

## 5\. 虛擬碼範例

以下使用類 Pascal 語法展示一個經典的「生產者-消費者問題」（Bounded-Buffer Problem）的監視器實作。

```pascal
monitor ProducerConsumer
    condition full, empty;
    integer count;

    procedure insert(item: integer);
    begin
        if count == N then wait(full); // 若緩衝區滿，等待 "full" 條件
        insert_item(item);
        count := count + 1;
        if count == 1 then signal(empty); // 喚醒等待 "empty" 的消費者
    end;

    procedure remove(var item: integer);
    begin
        if count == 0 then wait(empty); // 若緩衝區空，等待 "empty" 條件
        remove_item(item);
        count := count - 1;
        if count == N - 1 then signal(full); // 喚醒等待 "full" 的生產者
    end;

    { 初始化程式碼 }
    begin
        count := 0;
    end;
end monitor;
```

-----

## 6\. 與號誌 (Semaphore) 的比較

| 特性 | 監視器 (Monitor) | 號誌 (Semaphore) |
| :--- | :--- | :--- |
| **抽象層級** | 高階語言結構 | 低階系統呼叫 |
| **易用性** | 較容易，編譯器處理互斥 | 較難，需手動處理 P/V 操作 |
| **互斥控制** | 自動（隱式） | 手動（顯式） |
| **錯誤傾向** | 較低，結構化強 | 較高，易忘記釋放鎖導致死結 |
| **實作基礎** | 通常由編譯器或直譯器支援 | 作業系統核心提供 |