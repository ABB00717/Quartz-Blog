---
title: 14 Exception Handling and Event Handling
draft: true
tags:
  - programming-language
date: 
---
有例外處理（Exception Handling）才可以解決問題，連行程發生例外都無法偵測，那更談何解決問題？

# 大綱
- 基本要件
- 困境
- 控制流
- 程式語言實做
	- Ada
	- C++
	- Java 

# 例外處理的基本要件

- 例外偵測
- 例外處理（Exception Handler）

## 例外偵測
例外就是指那些在原本意料之外的事，通常沒有做好就容易成為資安破口。使用者輸入沒有 EOF 該怎麼辦？

## 例外處理
現代語言都有 `raised` 關鍵字，但就算沒有還是可以做例外處理。像是回傳特殊值、修改特殊狀態。

# 例外處理的困境
通常這種例外處理程式寫起來很無聊，可能還佔了你程式碼的一半行數。

而且在無限的使用者可能中，我該如何限制範圍，在範圍以外的例外又該如何應對？硬體錯誤算是例外嘛？對於沒有提供自己的例外處理機制的程式，是否應該有預設的例外處理器？

還有好多好多的問題

# 例外處理的控制流
![[exception handler control flow.png | 例外處理的控制流]]

在 Ada 中例外處理是和該子程序同個區塊內，因此不須任何參數傳遞。Ada 是當時例外處理做的數一數二好的語言。

不同區塊單元對沒有對應例外的程序也會有不同應對狀況

# 例外處理

## 預定義例外
- 範圍約束
- 數值錯誤
- 程式錯誤
- 儲存空間錯誤
- 任務處理錯誤

## `try-catch`
C++ 引入這種機制。

```cpp
- Exception Handlers Form:
try {
-- code that is expected to raise an exception
} catch (formal parameter) {
-- handler code
}
...
catch (formal parameter) {
-- handler code
}
```

`parameter` 不一定要是參數，它可以只是特別的型別，甚至可以是省略號（ellipsis），只要能和其他 `catch` 區塊區分就沒問題。

### 未處理的例外
如果該例外沒有被 `catch`，就會傳播給引發該例外的函數呼叫者，直到傳播到主函式後若都還沒有被接住，那程序就會中止。

### 延續執行
會從第一個狀態繼續執行

### 重新審視
但很多例外無法被命名，也無法被硬體軟體偵測到。透過參數類型將例外綁定到處理程序，無疑會降低可讀性。

## 例外類別（Java）
所有例外都是 `throwable` 的子類別

`throwable` 只有兩個子類別：
- 錯誤：程式錯誤
- 例外：使用者可以自訂處理方式

和 C++ 非常相向，但 Java 每個 `catch` 都必須有一個 `throwable` 型別的參數。常會搭配 `new` 運算子來建立例外物件。

### 例外與處理的綁定

### 延續執行
在其他封閉的 `try` 結構中找，以此類推。找不到再傳播到調用者，若一直到主程序都沒處理就中止。

所以為了確保所有例外都能被捕捉，可以在任何 `try` 結構中包含一個能捕捉所有例外的處理器。

### 受檢（Checked）和非受檢（Unchecked）例外
除了錯誤以及 RunTimeException 是非受檢以外，其他例外都是受檢例外。

### 其他設計
抓到了例外以後，你可以選擇：
- 處理它
- 把它換個形式丟出
- 不做任何事

#### `finally`
用於指定無論在 `try` 區塊中發生什麼情況都必須執行的程式碼

#### 斷言
可以用 `assert` 檢查一個布林表達式語句，若評估為假則拋出 AssertionError 例外。
- assert condition;
- assert condition: expression;

# 事件處理
事件（Event）是由外部動作驅動的，像是點擊 GUI 介面。事件處理器（Event Handler）就是處理這些事件的程式碼。

[Class EventHandler](https://docs.oracle.com/javase/8/docs/api/java/beans/EventHandler.html)

# 總結

- Ada 提供廣泛的例外處理機制，配備完整的內建例外集合。
- C++ 並未內建預定義的例外。例外是透過將 throw 語句中的表達式類型與 catch 函式之參數類型進行綁定來建立處理關聯
- Java 的例外機制與 C++ 類似，差別在於 Java 的例外必須是 Throwable 類別的子類。此外 Java 還包含 finally 子句
- 事件是指需要由事件處理器進行處理之特定情況發生的通知