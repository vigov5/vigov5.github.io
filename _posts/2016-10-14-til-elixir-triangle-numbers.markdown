---
layout: post
title:  "[TIL] Elixir with triangle-numbers"
date: 2016-10-14 09:59:26 +0700
categories: elixir til
---
(Đúng ra phải là **YIL** - *yesterday I learn*, nhưng thôi kệ vậy)

Yêu cầu: cho một số `x`, viết function in ra mảng sau:
{% highlight python %}
[[0], [1, 2], [3, 4, 5], ...]
{% endhighlight %}

Mảng con cuối cùng sẽ có chiều dài là `x`. Và đây là code python ban đầu của mình. Khá cùi bắp:

<!--description-->

{% highlight python %}
result = []
length = 0
for i in range(1, x + 1):
  result.append(range(i + length - i, i + length))
  length += i
{% endhighlight %}

ok, nếu xếp lại như sau:

{% highlight text %}
   0
  1 2
 3 4 5
6 7 8 9
{% endhighlight %}

Nó sẽ thành tam giác, google thử dãy `0, 1, 3, 6` ra ngay cả
[triangular number](https://en.wikipedia.org/wiki/Triangular_number) và [A000217](https://oeis.org/A000217).
Vậy bọn này sẽ có công thức tổng quát là:

$$a(n) = n*(n+1)/2$$ với $$n \geq 1$$

Tương tự phần tử cuối sẽ là:

$$b(n) = n*(n+1)/2 + n = n*(n+3)/2$$ với $$n \geq 1$$

Giờ chuyển qua code:

{% highlight elixir %}
def triangle_array(n) do
  Enum.map(0..n, fn(x) -> Enum.to_list round(x*(x+1)/2)..round(x*(x+3)/2) end)
end
{% endhighlight %}

Duy nhất 1 dòng, không cần biến tạm, so sexy !
