---
title: Scheme
draft: true
tags:
  - functional-programming
date: 2025-12-15
---

Java 全部東西都是類別，Scheme 什麼東西都是串列。

```scheme
(CAR `)
```

C 設計貼核組合語言，Scheme 簡潔為了貼核 Lambda Calculus

---

把串列想像成 Linked-List

```c
struct Node {
	void *data;
	struct Node *next;
}
```

就此引出 `cons` 的精確定義，它並不是單純的串接，而是建立一個新的節點，將兩個資料分別存放在 `data` 以及 `next` 裡頭。

```c
// cons(A, B)
Node* newNode = malloc(sizeof(Node));
newNode->data = A;
newNode->next = B; 
return newNode;
```

再由此引出 `cdr`  的精確定義。`cdr` 返回的是 `next` 指標。如果 `l` 是 `(5 (3 8))` ，那記憶體中就是 `[5] -> [(3 8)] -> NULL`。也因此 `cdr` 會回傳指向 `[(3 8)] -> NULL` 的指標，也就是 `((3 8))`。

> [!warning] 不是單純的 `(3 8)`！


## 範例
假設有個程式碼
```scheme
(define (mystery W)
  (cond
    ((number? W) '())
    ((number? (car W)) (cdr W))
    (else (cons (mystery (car W)) (cdr W)))
  )
)
```

換成 C-like 程式碼就是這樣

```c
Node* mystery(Node *W) {
    if (W == NULL || W->type == TYPE_NUMBER) {
        return NULL; // 返回空列表
    }
	
    if (W->data.list_head != NULL && W->data.list_head->type == TYPE_NUMBER) {
        return W->next; 
    } else {
        Node *result_of_car = mystery(W->data.list_head);
        Node *rest_of_list = W->next;
        return cons(result_of_car, rest_of_list); 
    }
}
```

假設呼叫 `(mystery '((9 8 (2 4)) (4 5))`：
- `w->data.list_head` = `(9 8 (2 4))`，不是 `NUMBER`，因此
	- `return cons(mystery((9 8 (2 4))) (4 5))`
- `w->data.list_head` = `[9]`，是 `NUMBER`，因此
	- `return (8 (2 4))`
- 回到 `return cons(mystery((9 8 (2 4))) (4 5))`
	- 變成 `cons((8 (2 4)) (4 5))`
		![[image-34.png]]
	- `( (8 (2 4)) ((4 5)) )`
- 最後變成 `(((8 (2 4)) (4 5)))`

---

- `cons`：建構元素與串列
- `car`：取首
- `cdr`：取除首外的剩餘串列
- `list`：接收多個參數，並將其聚合成一個新的串列

> [!note] `car` 和 `cdr` 是啥意思？
> `car`: Contents of the Address part of Register
> `cdr`: Contents of the Decrement part of Register
>
> 參見 IBM 704 的 36 位元字組架構。
> %%補上 IBM 704 的 36 位元字組架構%%