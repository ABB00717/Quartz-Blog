---
title: 14 Exception Handling and Event Handling
draft: false
tags:
  - programming-language
date:
---
例外處理（Exception Handling）是解決程式問題的核心機制。若無法偵測行程中發生的異常，便無法著手解決問題。本文將探討例外處理的基本要件、面臨的困境、控制流設計，以及在不同程式語言（Ada、C++、Java）中的實作方式。

# 大綱
- 基本要件
- 困境
- 控制流
- 程式語言實做
	- Ada
	- C++
	- Java 

# 基本要件

例外處理機制主要包含兩個部分：

- **例外偵測 (Exception Detection)**
  例外指的是程式執行過程中發生的非預期事件。若未妥善處理，容易演變成資安漏洞。例如：當程式預期讀取資料卻未遇到 EOF（End of File）時，該如何應對？
- **例外處理 (Exception Handler)**
  現代程式語言通常具備 `raise` 或 `throw` 關鍵字來觸發例外。即使在沒有內建機制的環境中，開發者仍可透過回傳特殊值或修改特定狀態旗標來實作例外處理。

# 例外處理的困境
通常這種例外處理程式寫起來很無聊，可能還佔了你程式碼的一半行數。而且在無限的使用者可能中，我該如何限制範圍，在範圍以外的例外又該如何應對？硬體錯誤算是例外嘛？對於沒有提供自己的例外處理機制的程式，是否應該有預設的例外處理器？

> 有趣的是，現在 LLM 的興起大幅降低程式碼撰寫成本，也讓更多程式設計師願意面對例外處理了。

# 例外處理的控制流
![[exception handler control flow.png]]

在控制流設計上，不同語言有不同策略。以 Ada 為例，其例外處理與子程序位於同一區塊內，因此不需要進行參數傳遞。Ada 在當時被視為例外處理機制設計最為完善的語言之一。針對不同單元中未捕捉到的例外，系統也會有相應的處理流程。

# 程式語言實做

## Ada

Ada 提供了豐富的預定義例外，涵蓋以下類型：

- 範圍約束 (Range constraints)
- 數值錯誤 (Numeric errors)
- 程式錯誤 (Program errors)
- 儲存空間錯誤 (Storage errors)
- 任務處理錯誤 (Tasking errors)

## C++
C++ 引入了 `try-catch` 機制。

**基本語法：**
```cpp
try {
    // 可能引發例外的程式碼
} catch (formal parameter) {
    // 處理程序
}
...
catch (formal parameter) {
    // 處理程序
}
```

`parameter` 不一定要是參數，它可以只是特別的型別，甚至可以是省略號（ellipsis），只要能和其他 `catch` 區塊區分就沒問題。
  
若例外未被當前的 `catch` 區塊捕捉，它將向外傳播給呼叫該函數的父層。若傳播至主函式（Main）仍未被處理，程式將會終止。 捕捉並處理後，程式將從 `catch` 區塊之後繼續執行。

### 重新審視
但很多例外無法被命名，也無法被硬體軟體偵測到。透過參數類型將例外綁定到處理程序，無疑會降低可讀性。

## Java（例外類別）

所有例外都是 `throwable` 的子類別

`throwable` 只有兩個子類別：
- 錯誤：程式錯誤
- 例外：使用者可以自訂處理方式

和 C++ 非常相向，但 Java 每個 `catch` 都必須有一個 `throwable` 型別的參數。常會搭配 `new` 運算子來建立例外物件。

**語法特性：**

  * 每個 `catch` 區塊必須接收一個 `Throwable` 型別的參數。
  * 通常搭配 `new` 運算子來建立例外物件。

**例外傳播與捕捉：**

  * 當例外發生時，系統會依序在封閉的 `try` 結構中尋找對應的處理器。若找不到，則向外層傳播，直到主程序。若最終未被處理，程式將終止。
  * 為確保穩健性，開發者可在最外層的 `try` 結構中加入通用的例外處理器。

**受檢例外 (Checked) 與非受檢例外 (Unchecked)：**

  * **非受檢例外**：包含 `Error` 與 `RuntimeException`。
  * **受檢例外**：除此之外的所有例外皆屬之，編譯器會強制要求處理。

**處理策略：**
捕捉到例外後，通常有三種選擇：

1.  處理它。
2.  轉換形式後重新拋出 (Rethrow)。
3.  忽略（不建議）。

**特殊結構：**

  * **`finally`**：無論 `try` 區塊內是否發生例外，`finally` 區塊內的程式碼保證會被執行（常用於資源釋放）。
  * **斷言 (`assert`)**：用於驗證布林表達式。若評估為 `false`，則拋出 `AssertionError`。
      * `assert condition;`
      * `assert condition: expression;`

# 事件處理
事件（Event）是由外部動作驅動的，像是點擊 GUI 介面。事件處理器（Event Handler）就是處理這些事件的程式碼。

> [!note] 參考資料：[Class EventHandler (Java Documentation)](https://docs.oracle.com/javase/8/docs/api/java/beans/EventHandler.html)

# 總結
  * **Ada**：提供廣泛且完整的內建例外集合。
  * **C++**：未內建預定義例外，透過 `throw` 表達式型別與 `catch` 參數型別的綁定來建立處理關聯。
  * **Java**：機制類似 C++，但強制例外必須繼承自 `Throwable`，並區分受檢/非受檢例外，且引入了 `finally` 區塊以確保資源清理。
  * **事件**：指特定情況發生的通知，需由事件處理器進行回應。