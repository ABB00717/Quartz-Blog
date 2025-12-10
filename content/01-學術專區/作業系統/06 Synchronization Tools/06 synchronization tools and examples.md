---
title: 00 Semophore & Synchronization
draft: true
tags:
  - operating-system
date: 2025-12-09
---

# 大綱
- 旗號實作
- 旗號的四種經典用途
- 優先反向（Priority Inversion）
- 死結與飢餓（Deadlock and Starvation）
- 監視器（Monitor）
- Bounded-Buffer Problem

# 旗號實作
Semaphore （$S$ ）本質上就只是一個整數變數。只是它只能透過原子操作 `wait` 和 `signal` 來存取。

> [!cite] 雖然我還是習慣叫它 $P()$ 和 $V()$

## Busy Waiting
等嘛，那最土砲的方式當然就是搞一個無限迴圈。
```c
wait(S) {
    while (S <= 0)
        ; // 一直在這裡空轉，吃 CPU 資源
    S--;
}
```

不要看它好像很白痴，如果 Critical Section 很長那它確實很浪費 CPU Cycle，而且因為它會一直佔用資源，單處理器絕對不能用。但如果鎖的時間很短，它真的比 Context Switch 還快。

## Wait and Signal
不要無意義的空轉，讓它停（Sleep/Block），但停了之後要重新喚醒。

```c
typedef struct {
    int value;
    struct process *list; // 等待隊列
} semaphore;

wait(semaphore *S) {
    S->value--;
    if (S->value < 0) {
        add_to_list(S->list);
        block(); // 讓出 CPU，進入 Waiting State
    }
}

signal(semaphore *S) {
    S->value++;
    if (S->value <= 0) {
        remove_from_list(S->list);
        wakeup(P); // 喚醒等待中的 Process
    }
}
```

> [!warning] `wait` 和 `signal` 一定要是一套的

# 旗號的四種經典用途

## 互斥鎖
`Semaphore` 初始值一定是 1，就是只有一個行程可以進去 CS，故得互斥此名。

```
wait(mutex)
// CS
signal(mutex)
```

## 資源計數
就是把 `Semaphore` 初始值改成 `N` 而已。

## 通知同步
一個行程結束了才會呼叫另一個行程進來，以此保證順序。

## 倒數鎖
`Semaphore` 初始化為 0，等到滿了以後最後一個到達的行程負責發送 `signal`

> 一直在想我生活中該怎麼運用這種鬼東西

# 優先權反轉
[火星探路者號就發生過這個問題](https://nerdyelectronics.com/priority-inversion-problem-and-solution)

總之就是，有一把鎖，低（L）優先權的行程拿著那把唯一的鎖。而這時高（H）優先權的想進入 CS，然而鎖卻被 L 佔著。更靠北的是，這時有個中（M）優先權的行程進來了，因為 M 優先權比 L，所以 M 搶佔了 L 的 CPU。這時 L 就不能跑，所以 H 就永遠拿不到鎖，就造成了明明 H 比 M 高，但卻被 M 卡死。

**優先權繼承（Priority Inheritance）**
這時，系統會把 L 的優先權提到和 H 一樣高。

# 死結與飢餓
- 死結：兩個以上的行程互相等待對方釋放資源，導致大家都卡死。
- 飢餓：無限期的阻擋 (Indefinite blocking)。行程可能一直在旗號的 Queue 裡面排隊，永遠輪不到它出來（例如 LIFO 的佇列策略可能導致先進去的人最後才出來，甚至出不來）。

# 監視器
[[monitor]]

旗號雖然強大，但它像是一把「低階的槌子」。程式設計師必須手動在各個地方呼叫 `wait()` 和 `signal()`。只要你忘記寫、寫錯順序、或是邏輯有漏洞（例如在 Critical Section 裡面當機），整個系統就會死結或資料毀損。

有 Monitor 這個抽象資料型別：
- 把共享變數和函式封裝
- 旗號是司有的，只能操作封裝好的函式
- 自動互斥

%%但具體範例呢？？？沒有真實的程式碼使用情境我怎麼會知道%%


範例：
```
Monitor example {
	int count;
	void Increase(void){
		count++;
	}

	void Decrease(void){
		count--;
	}
	
	int GetData(void){
		return count;
	}

	Init {count = 0;}
}
```

會自動判別 `condition x` 來確定要做 `wait` 還是 `signal`。每個 `x` 都有自己的等待序列，如果 `wait` 就會被暫停並返回序列，等到有行程 `signal` 就會被丟回 ReadyQueue。而如果 `signal` 沒有其他行程在等就會直接消失。

![[image-8.png]]

**Signal Semantics**

- Signal and Wait：
  在 $P$ `signal`  以後，如果真的有 $Q$ 在等，那 $P$ 就會馬上 `wait`，並且待在 `next` 裡面
- Signal and Continue

## 實作管程
- `mutex` (Semaphore, init=1)：控制誰能進入 Monitor 的大鎖 。
- `next` (Semaphore, init=0)：這是一個專門給「發出 Signal 後暫時讓出的 Process」掛網用的等待區 。
- `next_count` (int, init=0)：紀錄有多少人在 `next` 上面排隊

基本函式 $F$ 的實做會被 Monitor 包成這樣
```c
wait(mutex); // 進來先搶鎖
// ... body of F ...
// 離開時的處理：
if (next_count > 0)
    signal(next); // 優先讓之前發出 signal 而暫停的人回來執行
else
    signal(mutex); // 沒那種人的話，才開放外面排隊的新人進來
```

```c
// x.wait()
x_count++; // 紀錄我在等 x
if (next_count > 0) // 如果有那種「發完 signal 暫停的人」，叫他回來接手
    signal(next);
else
    signal(mutex); // 不然就開放外面的人進來

wait(x_sem); // 我自己去 x 的小房間睡覺
x_count--; // 醒來後，把紀錄消掉
```

%%為什麼這個最開始還要 `x_count`？啊這個 `x_sem` 又是三小？小房間又是三小？等待序列？不是啊為什麼他要等？不是應該

```
如果 Monitor 內已經有人
	那我待在 `next` 等待序列裡面等
否則
	好耶直接進去摟
```

這樣嘛？%%

```c
if (x_count > 0) { // 只有在真的有人等的時候才做動作
    next_count++; // 我因為要叫醒人，我自己要去 next 排隊，所以計數 +1
    signal(x_sem); // 叫醒等 x 的那個人
    wait(next); // 我自己去 next 睡覺 (Signal and Wait)
    next_count--; // 醒來後，計數 -1
}
```

%%
啊這裡也是啊，這不是應該要
```
如果還有其他人在 `next` 裡面
	 用 signal 叫它
```
這樣嘛？這麼複雜是三小？
%%

[[Semaphore 印表機]]

# Bounded-Buffer Problem
## Producer and Consumer Problem
- If buffer is full, producers should be blocked
- If buffer is empty, consumers should be blocked

```
int mutex = 1;
int full = 0;
int empty = N;
```

> [!note] `mutex` 一定要在最裡面 `wait` 和 `signal`，不然會死結。
> 假設生產者先鎖住 `mutex`，結果 `empty` 發現裡面是空的就會一直停在那。但這時因為 `mutex` 被鎖住，所以生產者沒辦法進去填充緩衝區。
## Reader-Writers Problem
- 很多個讀者可以一起讀，但一次只能有一個寫手寫
- 如果有讀者在讀，寫手就不能寫。反之，若有寫手在寫，則沒有讀者可讀
- 讀者有較高的優先權

假設有個鎖 `wrt`：
- 讀者：
	- `readcount` 紀錄
	- 第一個讀者要負責搶 `wrt`
	- 最後一個讀者要釋放 `wrt`，並且通知寫手
- 寫手：
	- 直接搶 `wrt`

![[image-9.png|246x189]]

![[image-10.png|281x315]]

## Dining-Philosophers Problem
假設所有人都拿左邊的筷子，那就沒人能吃飯了。解法其實很簡單
- 不要讓所有人都拿同一邊
- 不要讓桌子坐滿
- 用監視器解決

![[image-11.png|341x515]]

- `test` 中的 `signal` 在 `pickUp` 沒有效果，是為了在 `putDown` 中讓左右兩邊的人可以從 `wait` 中喚醒

> [!quote] 這些虛擬碼的實現非常重要，因為也只能考這個，所以不只期末考會考，你研究所考試也大概會考。