---
title: 自然語言程式設計
draft: true
tags:
  - programming-language
date: 2025-12-09
---

與高階語言不同，這真的是用自然語言的句子拼湊成的程式。

- [小說](https://en.wikipedia.org/wiki/Inform#Inform)
- [莎士比亞自然語言](https://en.wikipedia.org/wiki/Shakespeare_Programming_Language)
- [你我都十分熟悉的 Wolfram Alpha](https://www.wolframalpha.com/)

但我想的不一樣，我想的是能把任何自然語言「和編譯器一樣」直接翻譯成高階語言（或機器語言也行）的技術。

現在看起來 LLM 應該能完美達成這種任務。不過我在想，現在的流程比較像是我們直接下達簡單的句子與段落，單純描述需求。

但我想的是，能夠有個工具，讓使用者能夠只寫「虛擬碼」就可以讓 LLM 接手剩下的所有任務。

```
// brainfuck-interpreter.cpp

input_char: 不斷讀取輸入
tapes：一串紙帶，每格都可儲存正整數 
point: 指向紙帶的格子，初始為 tapes 的第 0 格

判斷 input_char:
	這是 '+', '-' 就在 point 指向的格子做 +1 或 -1
	這是 '.', ',' 就輸出或輸入 point 格子的數值
	如果這是 '>', '<' 就移動 point
	如果這是 ']' 遇到 ] 就判斷現在 point 這格的數字是否為 0
		若是則回到上個對應的 [，
		否則跳脫這個迴圈
```

像是這篇研究：[AIOS Compiler: LLM as Interpreter for Natural Language Programming and Flow Programming of AI Agents](https://arxiv.org/abs/2405.06907) 我覺得就超酷。

但我覺得不需要這麼極端，我認為應該會是像「只寫程式碼的註解」，而我們也可以寫一點高階語言來輔助。重點在於你不必再把自己的思路轉換成固定的高階語言，而是可以照任何自己舒服的方式來撰寫程式。

> [!question] 現在的 AI 驅動程式碼編輯器不就可以做到嗎？
> 是，但又有哪些人是用這種心態來寫程式的呢？

# 文學程式設計

其實早在 1984 年，Donald Knuth 就已提出類似概念，叫做[文學程式設計](https://en.wikipedia.org/wiki/Literate_programming)。

> [!cite] 與傳統程式設計的差異
> 這與傳統文件截然不同──傳統方式中，程式設計師面對的是遵循編譯器強制順序的原始碼，必須從程式碼及其相關注釋中解讀背後的思考歷程。文學化程式設計的元語言能力也被認為有助於思考，提供更高層次的「鳥瞰視角」，提升心智能成功保留與處理的概念數量。

> [!cite] 與文件生成的差異
> 「文學化編程」常被誤解為僅指從原始碼與註解共同組成的文件中產生的格式化文件——此類過程應正確稱為文件生成——或是指夾雜在代碼中的大量註解。這實際上與文學化編程的概念相悖：完善的代碼註解或從代碼提取的文件是遵循代碼結構，將文件嵌入代碼中；而文學化編程則是將代碼嵌入文件中，讓代碼遵循文件的結構。

# Computational Thinking
這大概是程式設計的終點。程式設計中，[Computational Thinking](https://www.cs.cmu.edu/~15110-s13/Wing06-ct.pdf)本就是最重要的一環，用什麼手段、程式語言其實是次要問題。

機器需要固定、統一的語法才能看懂指令，人類的思維卻是各異、發散的。現在 LLM 可以當作中間翻譯官，把各種各樣的自然語言翻譯成機器看得懂的語法。