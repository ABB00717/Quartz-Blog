---
title: 在樹梅派上建立自己的靶機
draft: true
tags:
  - raspberrypi
date: 2025-12-09
---
# 樹梅派
Imager

選 Ubuntu Server

ssh 
`keygen`

登入

```shell
nmap -sn 192.168.1.0/24
```

```
abb00717@ABB00717:~$ ssh abb00717@192.168.1.117
The authenticity of host '192.168.1.117 (192.168.1.117)' can't be established.
ED25519 key fingerprint is SHA256:xIXqywu6L3dvcWoiTbCiY2APetqVApZ6mUArvvXEljE.
This host key is known by the following other names/addresses:
    ~/.ssh/known_hosts:13: [hashed name]
Are you sure you want to continue connecting (yes/no/[fingerprint])? 
```

要刪除 `known_hosts` 中的第 13 行

```shell
sed -i '13d' ~/.ssh/known_hosts
```

[[id_ed25519]]
# 環境

https://hub.docker.com/r/cambarts/arm-dvwa
> Damn Vulnerable Web Application (DVWA) is a PHP/MySQL web application that is damn vulnerable. Its main goal is to be an aid for security professionals to test their skills and tools in a legal environment, help web developers better understand the processes of securing web applications and to aid both students & teachers to learn about web application security in a controlled class room environment.
