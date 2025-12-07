---
title: Example Title
publish: false
tags:
  - vim
date:
---
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