---
title: Vim
draft: true
tags:
  - vim
date:
---
# 常用快捷鍵


## 基礎跳轉

|指令     |功能     |
| --- | --- |
|`ctrl + i`     |回到上一個檔案     |
|`ctrl + o`     |前進到下一個檔案     |
|`g;`     |回到上次修改的位置     |
|`gi`     |回到上次修改的位置並進入插入模式     |


# Substitute

有時候會想要把某個東西「拿出來」放到別的地方。這時就可以用 `(...)`！

```
Expect: ab8 hahaha
Expect:   cc hahaha
Expect:     hahahahaa hahaha
Expect: TG()"*@&#O hahaha

:'<,'>s/Expect: *\(.* \)\(.*\)/\2 \1

hahaha ab8 
hahaha cc 
hahaha hahahahaa 
hahaha TG()"*@&#O 
```

# Command
套用指令

```
:g/^$/d
```