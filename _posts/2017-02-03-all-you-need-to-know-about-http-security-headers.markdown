---
layout: post
title:  "Tất cả những thứ bạn cần biết về HTTP security headers"
date: 2017-02-03 12:34:56 +0700
categories: security web
---

X-post: [https://viblo.asia/vigov5/posts/mDYGDPLVGpx](https://viblo.asia/vigov5/posts/mDYGDPLVGpx)

# Intro
```bash
[vigo@ubuntu ~]$ curl --head https://www.google.com.vn
HTTP/1.1 200 OK
Date: Fri, 03 Feb 2017 01:24:33 GMT
Expires: -1
Cache-Control: private, max-age=0
Content-Type: text/html; charset=ISO-8859-1
P3P: CP="This is not a P3P policy! See https://www.google.com/support/accounts/answer/151657?hl=en for more info."
Server: gws
X-XSS-Protection: 1; mode=block
X-Frame-Options: SAMEORIGIN
Set-Cookie: NID=96=TsQp1_XrR3bIyB_amPMFfgDMTP2jH42gOiwOxXygRjlUjgqJltTGqirrT5mwbaSuB0xBM0BqLKeA9ayR3Q34du-gV4t59W9mxufP_ufYiVf-x4v2f9Zqt970hIZQBfHD; expires=Sat, 05-Aug-2017 01:24:33 GMT; path=/; domain=.google.com.vn; HttpOnly
Alt-Svc: quic=":443"; ma=2592000; v="35,34"
Transfer-Encoding: chunked
Accept-Ranges: none
Vary: Accept-Encoding
```
Chắc hẳn chúng ta đã không ít lần nhìn thấy những HTTP security headers ví dụ như `X-XSS-Protection` hay `X-Frame-Options` ở trên và tự hỏi chúng có tác dụng gì ?
Bài viết này dịch và tổng hợp từ bài gốc tại [đây](https://blog.appcanary.com/2017/http-security-headers.html) hi vọng sẽ đem đến cho mọi người những kiến thức cơ bản nhất về chúng để có thể sử dụng hiệu quả và đúng cách.

<!--description-->

# HTTP Security Headers
## X-XSS-Protection

```
X-XSS-Protection: 0;
X-XSS-Protection: 1;
X-XSS-Protection: 1; mode=block
```

### Tại sao ?

**Cross Site Scripting** thường được viết tắt là **XSS** là một kiểu tấn công mà người tấn công sẽ khiến cho trang web chạy một đoạn javascript độc hại (cụ thể hơn về kiểu tấn công cũng như cách phòng chống, bạn có thể đọc series tuyệt vời về XSS của bạn [@Anh Tranngoc](https://viblo.asia/u/naa), link ở phần tham khảo).  `X-XSS-Protection` là một tính năng của trình duyệt Chrome và Internet Explorer, được thiết kế để chống lại **reflected” XSS attacks** - khi mà kẻ tấn công gửi mã độc hại như là một phần của request (reflected nghĩa là những gì bạn request lên sẽ được phản ánh lại qua nội dung trang web)

- `X-XSS-Protection: 0` : tắt chế độ này
- `X-XSS-Protection: 1` : lọc bỏ các đoạn scrip ở trong request, nhưng vẫn hiển thị trang web
- `X-XSS-Protection: 1; mode=block` : khi được kích hoạt sẽ vô hiệu hoàn toàn việc hiển thị trang web

### Tôi có nên dùng nó không ?

Có. Hãy thiết lập `X-XSS-Protection: 1; mode=block`. Các chế độ khác có thể gây vấn đề, lí do tại [đây](http://blog.innerht.ml/the-misunderstood-x-xss-protection/)

### Làm như thế nào ?

| Platform | Tôi cần làm gì ? |
|-|-|
|Rails 4 and 5	| Mặc định được bật |
| Django | `SECURE_BROWSER_XSS_FILTER = True` |
| Express.js | Sử dụng [helmet](https://helmetjs.github.io/docs/xss-filter/) |
| Go | Sử dụng  [unrolled/secure](https://github.com/unrolled/secure) |
|Nginx	| `add_header:  X-XSS-Protection "1; mode=block";` |
|Apache	| `Header always set X-XSS-Protection "1; mode=block"` |

### Tôi muốn biết thêm

[X-XSS-Protection - MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-XSS-Protection)

---

## Content Security Policy (CSP)

```
Content-Security-Policy: <policy>

```

### Tại sao?

**Content Security Policy** có thể được coi là một phiên bản nâng cao của X-XSS-Protection header ở trên. Trong khi X-XSS-Protection sẽ cản toàn bộ các  scripts đi kèm với request nhưng nó sẽ không thể cả được những tấn công XSS mà sẽ lưu lại script độc hại trên server của bạn hoặc tải từ một nguồn khác chứa sript độc hại trong đó.

CSP cho bạn ngôn ngữ để chỉ ra những nơi mà trình duyệt được phép tải tài nguyên về. Bạn có thể định nghĩa một danh sách các nguồn scripts, ảnh, font chữ, css cho từng cái một, cũng như kiểm tra hash của các tài nguyên đã được tải đó với chữ kí có sẵn.

### Tôi có nên dùng nó không ?

Có. Nó không thể ngăn chặn toàn bộ các tấn công XSS  nhưng nó đóng vai trò quan trọng trong việc hạn chế ảnh hưởng của chúng và là một khía cạnh quan trọng trong cả quá trình phòng thủ theo chiều sâu. Tuy nhiên, việc implement nó có thể là khá khó. Ví dụ như ở [appcanary.com](https://appcanary.com) chúng tôi cũng chưa thiết lập CSP vì đang có một vài plugin của rails đang dùng khiến việc thiết lập CSP chưa thể tiến hành. Chúng tôi đang làm việc và sẽ viết về vấn đề này trong thời gian tới.

### Làm như thế nào ?

Để viết được policy của CSP  có thể là một thách thức không nhỏ. Bạn có thể xem ở [đây](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy) để có danh sách các chỉ thị.
[Đây](https://csp.withgoogle.com/docs/adopting-csp.html) cũng là một điểm khởi đầu khá tốt.

|Platform|Tôi cần làm gì ?|
|-|-|
|Rails 4 and 5|Sử dụng [secureheaders](https://github.com/twitter/secureheaders)|
|Django|Sử dụng [django-csp](https://github.com/mozilla/django-csp)|
|Express.js|Sử dụng [helmet/csp](https://github.com/helmetjs/csp)|
|Go|Sử dụng [unrolled/secure](https://github.com/unrolled/secure)|
|Nginx|`add_header Content-Security-Policy "<policy>";`|
|Apache|`Header always set Content-Security-Policy "<policy>"`|

### Tôi muốn biết thêm

- [Content-Security-Policy - MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy)
- [CSP Quick Reference Guide](https://content-security-policy.com/)
- [Google&rsquo;s CSP Guide](https://csp.withgoogle.com/docs/index.html)

---

## HTTP Strict Transport Security (HSTS)

```
Strict-Transport-Security: max-age=<expire-time>
Strict-Transport-Security: max-age=<expire-time>; includeSubDomains
Strict-Transport-Security: max-age=<expire-time>; preload

```

### Tại sao?

Khi chúng ta thiết lập kết nối bảo mật với ai đó, chúng ta gặp phải 2 vấn đề. Thứ nhất là riêng tư: chúng ta chỉ muốn thông điệp đó được nhìn thấy bởi người nhận chứ không phải là bất cứ một người nào khác, Vấn đề còn lại là xác thực: làm sao để biết được người nhận chính là người mà họ nói họ là người đó.

HTTPS giải quyết được vấn đề đầu tiên bằng cách mã hoá nhưng lại gặp một số vấn đề lớn với việc xác thực (bàn kĩ hơn ở mục Public Key Pinning). HSTS header giải quyết được vấn đề ban đầu: làm sao bạn biết được người mà bạn đang nói chuyện  đang thực sự hỗ trợ việc mã hoá ?

Sử dụng HSTS, chúng ta có thể chống lại được kiểu tấn công [sslstrip](https://moxie.org/software/sslstrip/). Ví dụ: bạn đang sử dụng mạng đi thuê nhưng không may, kể tấn công chiếm được quyền kiểm soát router wifi. Hắn có thể vô hiệu hoá việc mã hoá giữa bạn và trang web bạn đang xem. Cho dù là trang web đó chỉ có thể truy cập qua HTTPS nhưng kẻ tấn công vẫn có thể là người đứng giữa (man-in-the-middle) loại bỏ (strip) phần HTTPS và làm cho nó giống như trang đang hoạt động qua HTTP. Không cần chứng chỉ SSL, chỉ là tắt bỏ phần mã hoá.

Sử dụng Strict-Transport-Security header giải quyết vấn đề này bằng cách cho trình duyệt biết là chúng phải luôn luôn dùng mã hoá với trang của bạn. Chừng nào mà trình duyệt còn thấyt HSTS header và header đó chưa hết hạn thì nó sẽ không truy cập trang thông qua HTTP và sẽ báo lỗi nếu trang đó không truy cập được qua HTTPS.

### Tôi có nên dùng nó không ?

Có. App của bạn chỉ hoạt động qua HTTPS, đúng không? Nếu truy cập đến HTTP thì sẽ bị chuyển sang phía HTTPS đúng không ? (Gợi ý: Sử dụng [letsencrypt](https://letsencrypt.org/))

Có một vấn đề nhỏ là sử dụng HSTS một cách khéo léo có thể cho phép bạn tạo ra [supercookies](http://www.radicalresearch.co.uk/lab/hstssupercookies) có thể dùng để theo dấu người dùng. Là quản trị viên thì rất có thể là bạn đang track người dùng rồi, tuy nhiên chúng tôi khuyến cáo bạn không dùng HSTS để tạo supercookies.

### Làm như thế nào ?

Có hai lựa chọn sau

- `includeSubDomains` - HSTS áp dụng cho cả subdomains
- `preload` - Google có một [dịch vụ](https://hstspreload.appspot.com/)
sẽ ghi cứng rằng app của bạn chỉ truy cập bằng HTTPS. Bằng cách này, người dùng không cần phải truy cập vào trang của bạn vì trình duyệt đã biết trước điều này và sẽ từ chối các kết nối không được mã hoá. Để ra khỏi danh sách này khá khó nên hãy bật nó lên chỉ khi đảm bảo là bạn có thể hỗ trợ HTTPS cho trang của bạn cùng với subdomain trọn đời.

|Platform|Tôi cần làm gì ?|
|-|-|
|Rails 4| `config.force_ssl = true`.<br>Không bao gồm cho subdomain. Để thiết lập cả cho subdomain, làm như sau:<br> `config.ssl_options = { hsts: { subdomains: true } }`|
Rails 5| `config.force_ssl = true`|
|Django| `SECURE_HSTS_SECONDS = 31536000`<br>`SECURE_HSTS_INCLUDE_SUBDOMAINS = True`|
|Express.js|Sử dụng [helmet](https://helmetjs.github.io/docs/hsts/)|
|Go|Sử dụng [unrolled/secure](https://github.com/unrolled/secure)|
|Nginx|`add_header Strict-Transport-Security "max-age=31536000; includeSubdomains; ";`|
|Apache|`Header always set Strict-Transport-Security "max-age=31536000; includeSubdomains;`|

### Tôi muốn biết thêm

- [RFC 6797](https://tools.ietf.org/html/rfc6797)
- [Strict-Transport-Security - MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security)

---

## HTTP Public Key Pinning (HPKP)

```
Public-Key-Pins: pin-sha256=<base64==>; max-age=<expireTime>;
Public-Key-Pins: pin-sha256=<base64==>; max-age=<expireTime>; includeSubDomains
Public-Key-Pins: pin-sha256=<base64==>; max-age=<expireTime>; report-uri=<reportURI>

```

### Tại sao?

HSTS header được thiết kế để đảm bảo rằng tất cả các kết nốt đến web site của bạn được mã hoá. Tuy nhiên không có chỗ nào miêu tả khoá để sử dụng cả !

Sự tin tưởng ở trên web hiện nay được xây dựng thông qua mô hình certificate authority (CA).
Hệ điều hành và trình duyệt của bạn đã có sẵn những khoá công khai (public keys) của những nhà phát hành  chứng chỉ  uy tín (trusted certificate authorities) thường là những công ty chuyên môn hoặc là của chính phủ. Khi một CA phát hành một chứng chỉ cho một tên miền (domain) nghĩa là bất cứ ai tin tưởng nhà phát hành đó đều sẽ tự động tin tưởng những kết nối SSL được mã hoá bởi chứng chỉ đó. Những nhà cung cấp chứng chỉ này có trách nhiệm phải xác nhận rằng bạn thực sự là chủ của tên miền đó ( có thể  bằng cách yêu cầu bạn gửi email, hoặc host một tệp tin hoặc, điều tra về công ty của bạn).

Hai nhà cung cấp chứng chỉ hoàn toàn có thể phát hành chứng chỉ cho một tên miền cho 2 người khác nhau, và như vậy, trình duyệt cũng sẽ tin tưởng cả hai. Việc này tạo ra một vấn đề, đặc biệt là khi [nhà cung cấp đó (có thể và) bị làm tổn hại](https://technet.microsoft.com/library/security/2524375). Khi đó, kẻ tấn công có thế thực hiện tấn công man-in-the-middle (MiTM) bất cứ tên miền nào hắn muốn, cho dù là tên miền đó có sử  dụng SSL và HSTS !

HPKP header được sinh ra nhằm giải quyết vấn đề này. Header này cho phép bạn "pin" (gắn) chứng chỉ với tên miền. Khi trình duyệt thấy header này, nó sẽ lưu lại chứng chỉ. Đối với mỗi request cho đến thời điểm `max-age`, trình duyệt sẽ không tải trang trừ khi có ít nhất một chứng chỉ trong chỗi chứng chỉ mà server trả về  là cái đã được pin.

Điều này nghĩa là bạn có thể pin tới một CA hoặc là chứng chỉ trung gian đi kèm với chứng chỉ cuối cùng để tránh tự bắn vào chân mình (cụ thể ở  sau đây).

Cũng giống như HSTS, HPKP header cũng có vấn đề liên quan đến quyền riêng tư được miêu tả  ở tài liệu này [RFC](https://tools.ietf.org/html/rfc7469#section-5)

### Tôi có nên dùng nó không ?

Có lẽ là không.

HPKP thực sự là một con dao rất rất sắc. Thử nghĩ như sau: nếu chẳng may bạn pin nhầm chứng chỉ, hoặc là bạn làm mất khoá của mình  hoặc có điều gì đó không đúng, bạn sẽ khiến người dùng không thể truy cập đến trang của bạn. Tất cả bạn có thể làm là ngồi chờ cho đến khi pin hết hiệu lực.

[Tài liệu này](https://blog.qualys.com/ssllabs/2016/09/06/is-http-public-key-pinning-dead) có miêu tả chi tiết hơn các tình huống, nó cũng miêu tả  một cách rất hài hước, cách mà kẻ tấn công có thể sử dụng HPKP để tống tiền nạn nhân của chúng.

Có một cách khác, đó là chỉ sử dụng `Public-Key-Pins-Report-Only` header, nghĩa là chỉ thông báo rằng có gì đó không đúng thay vì chặn mọi người truy cập. Việc này sẽ báo cho bạn biết rằng người dùng trang web của bạn đang bị tấn công MiTM bằng chứng chỉ giả.

### Làm như thế nào ?

Bạn có 2 lựa chọn:

- `includeSubDomains` - HPKP  áp dụng cho cả các subdomains
- `report-uri` - Những request có vấn đề sẽ được thông báo tớ địa chỉ này

Bạn phải tạo vân tay đã mã hoá base64 (base64 encoded fingerprint) cho khoá bạn muốn pin và bạn **bắt buộc** phải dùng khoá dự phòng. Tham khảo [hướng dẫn](https://developer.mozilla.org/en-US/docs/Web/HTTP/Public_Key_Pinning#Extracting_the_Base64_encoded_public_key_information)
sau để biết chi tiết cách làm.

|Platform|Tôi cần làm gì ?|
|-|-|
|Rails 4 and 5|Sử dụng [secureheaders](https://github.com/twitter/secureheaders/blob/master/docs/HPKP.md)|
|Django| Viết middleware riêng|
|Express.js|Sử dụng [helmet](https://helmetjs.github.io/docs/hpkp/)|
|Go|Sử dụng [unrolled/secure](https://github.com/unrolled/secure)|
|Nginx|`add_header Public-Key-Pins 'pin-sha256="<primary>"; pin-sha256="<backup>"; max-age=5184000; includeSubDomains';`|
|Apache|`Header always set  Public-Key-Pins 'pin-sha256="<primary>"; pin-sha256="<backup>"; max-age=5184000; includeSubDomains';`|

### Tôi muốn biết thêm

- [RFC 7469](https://tools.ietf.org/html/rfc7469)
- [HTTP Public Key Pinning (HPKP) - MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Public_Key_Pinning)

---

## X-Frame-Options

```
X-Frame-Options: DENY
X-Frame-Options: SAMEORIGIN
X-Frame-Options: ALLOW-FROM https://example.com/

```

### Tại sao?

Trước khi chúng ta bắt đầu đưa ra những cái tên ngớ ngẩn cho các loại lỗ hồng thì chúng ta cũng đã từng đưa ra nhưng cái tên như vậy cho các kĩ thuật tấn công. &ldquo;Clickjacking&rdquo; là một cái tên như vậy.

Ý tưởng của kĩ thuật này như sau: bạn tạo một frame "tàng hình" trên trang, đưa nó vào focus và điều hướng để người dùng thao tác với nó. Là kẻ tấn công, bạn hoàn toàn có thể lừa người dùng chơi 1 game trên trình duyệt, trong khi bí mật ghi lại những click của họ vào một iframe hiển thị twitter, buộc họ retweet tất cả những tweets của bạn mà họ không hề hay biết.

Nghe có vẻ ngớ ngẩn nhưng đây là một cách tấn công hiệu quả.

### Tôi có nên dùng nó không ?

Có. Không ai muốn app của mình bị đưa và iframe và bị dùng cho những mục đích không mong muốn, ví dụ như ở [đây](https://techcrunch.com/2015/04/08/annotate-this/) rồi.

### Làm như thế nào ?

**X-Frame-Options** có 3 chế độ như sau:

- `DENY` - Không ai có thể  đặt trang này vào một iframe
- `SAMEORIGIN` - Trang chỉ có thể được hiển thị ở trong một iframe tạo bởi ai đó ở cùng một nguồn (same origin) với nó.
- `ALLOW-FROM` - Chỉ định đường dẫn url có thể đặt trang này vào iframe.

Một điều nên nhớ là bạn có thể chồng iframe (iframe trong iframe..) bao nhiêu tuỳ thích, trong trường hợp này, biểu hiện của `SAMEORIGIN` và `ALLOW-FROM` là [chưa được chỉ định](https://tools.ietf.org/html/rfc7034#section-2.3.2.2). Đó là khi, chúng ta có 3 cái iframe lồng nhau và cái trong cùng thiết lập `SAMEORIGIN` thì nghĩa là ta đang quan tâm đến cái lồng ngay bên ngoài nó hay là cái ở ngoài cùng ??? ¯\\_(ツ)_/¯.


|Platform| Tôi cần làm gì ?|
|-|-|
|Rails 4 and 5| SAMEORIGIN mặc định được bật. Chuyển sang DENY như sau<br>`config.action_dispatch.default_headers[&#39;X-Frame-Options&#39;] = "DENY"`|
|Django| `MIDDLEWARE = [ ... 'django.middleware.clickjacking.XFrameOptionsMiddleware', ... ]` mặc định là SAMEORIGIN. <br>Chuyển sang DENY: `X_FRAME_OPTIONS = 'DENY'`|
|Express.js|Sử dụng [helmet](https://helmetjs.github.io/docs/frameguard/)|
|Go|Sử dụng [unrolled/secure](https://github.com/unrolled/secure)|
|Nginx|`add_header X-Frame-Options "deny";`|
|Apache|`Header always set  X-Frame-Options "deny"`|

### Tôi muốn biết thêm

- [RFC 7034](https://tools.ietf.org/html/rfc7034)
- [X-Frame-Options - MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options)

---

## X-Content-Type-Options

```
X-Content-Type-Options: nosniff;

```

### Tại sao?

Vấn đề  mà header này cố giải quyết là **&ldquo;MIME sniffing&rdquo;** mà thực ra là một "tính năng" của trình duyệt.

Về lý thuyết thì mỗi lần server của bạn trả lời một request thì nó phải thiết lập `Content-Type header` để báo với trình duyệt rằng nó đang nhận được HTML hay là ảnh gif hay là game Flash từ những năm 2008. Tuy nhiên, web thì không bao giờ là đồng nhất và theo sát một spec cố định, vào những ngày đó mọi người chưa biết cách để thiết lập content type header đúng cách.

Vì lý do đó, các nhà sản xuất trình duyệt web đã quyết định là họ sẽ thêm vào tính năng hữu ích: đoán xem nội dung nhận được là gì và bỏ qua chỉ định của content type header. Nếu thứ nhận được trông giống ảnh gif, ta hiển thị ảnh gif mặc dù content type là text/html đi chăng nữa. Tương tự, nếu nó trông giống HTML, thì ta sẽ hiển thị nó là HTML, cho dù server bảo là nó là ảnh gif đi chăng nữa.

Thật là tuyệt vời...cho đến khi bạn chạy một trang chia sẻ ảnh và người dùng có thể up lên một file ảnh mà trông giống HTML có kèm thêm javascript bên trong và Bùm !, trang của bạn đã bị XSS ! (chính xác là stored XSS)

X-Content-Type-Options headers xuất hiện để bảo với trình duyệt rằng: "hãy ngậm miệng lại và đặt content type theo đúng những gì tôi bảo, cảm ơn rất nhiều"

### Tôi có nên dùng nó không ?

Có, chỉ cần đảm bảo là bạn thiết lập content type một cách chính xác.

### Làm như thế nào ?

|Platform|Tôi cần làm gì ?|
|-|-|
|Rails 4 and 5| mặc định được bật|
|Django|`SECURE_CONTENT_TYPE_NOSNIFF = True`|
|Express.js| Sử dụng [helmet](https://helmetjs.github.io/docs/dont-sniff-mimetype/)|
|Go| Sử dụng [unrolled/secure](https://github.com/unrolled/secure)|
|Nginx| `add_header X-Content-Type-Options nosniff;`|
|Apache| `Header always set  X-Content-Type-Options nosniff`|

### Tôi muốn biết thêm

- [X-Content-Type-Options - MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options)

---

## Referrer-Policy

```
Referrer-Policy: "no-referrer"
Referrer-Policy: "no-referrer-when-downgrade"
Referrer-Policy: "origin"
Referrer-Policy: "origin-when-cross-origin"
Referrer-Policy: "same-origin"
Referrer-Policy: "strict-origin"
Referrer-Policy: "strict-origin-when-cross-origin"
Referrer-Policy: "unsafe-url"

```

### Tại sao?

**Referer header** rất tuyệt cho phân tích, nhưng tệ cho sự riêng tư của người dùng. Có thể là không phải là một ý tưởng tốt nếu cứ gửi nó lên ở mọi request.

`Referrer-Policy` header  cho phép bạn chỉ định khi nào thì trình duyệt sẽ thêm vào Referer header cùng với request gửi lên.

### Tôi có nên dùng nó không ?

Điều này phụ thuộc vào bạn, nhưng đây có thể là một ý tưởng tốt. Nếu bạn không quan tâm đến sự riêng tư của người dùng thì hãy nghĩ đây là một cách để bạn có riêng cho mình những phân tích đáng giá và tránh nó bị rơi vào tay đối thủ.

Hãy thiết lập `Referrer-Policy: "no-referrer"`

### Làm như thế nào ?

|Platform|Tôi cần làm gì ?|
|-|-|
|Rails 4 and 5|Sử dụng [secureheaders](https://github.com/twitter/secureheaders)|
|Django|Viết middleware riêng|
|Express.js|Sử dụng [helmet](https://helmetjs.github.io/docs/referrer-policy/)|
|Go|Viết middleware riêng|
|Nginx|`add_header Referrer-Policy "no-referrer";`
|Apache|`Header always set  Referrer-Policy "no-referrer"`|

### Tôi muốn biết thêm

- [Referrer Policy - MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy)

---

## Cookie Options

```
Set-Cookie: <key>=<value>; Expires=<expiryDate>; Secure; HttpOnly; SameSite=strict

```

### Tại sao?

Đây không phải là HTTP security header, tuy nhiên có nhiều options của cookie mà tôi nghĩ là bạn cũng nên biết.

- Cookies được đánh dấu là `Secure` sẽ chỉ  xuất hiện qua HTTPS. Việc này sẽ tránh được ai đó đọc nội dung của cookie bằng cách tấn công MiTM, nơi mà họ có thể buộc trình duyệt truy cập đến 1 trang.

- `HttpOnly` là một cái tên dễ gây hiểu lầm, và nó không liên quan gì đến HTTPS cả, (không giống `Secure` ở bên trên). Cookies được đánh dấu là `HttpOnly` không thể  bị truy cập từ javascript. Do đó, nếu có lỗi XSS thì kẻ tấn công cũng không thể ngay lập tức ăn cắp cookies này được.

- `SameSite` giúp chúng ta chống lại việc bị tấn công **Cross-Origin Request Forgery** (CSRF). Đây là kiểu tấn công khi người dùng trong lúc truy cập một trang web khác đã bị lừa tạo một request đến trang của bạn. Ví dụ như, thêm 1 ảnh để tạo 1 GET request hoặc dùng javascript để submit form từ một POST request. Thông thường thì mọi người sẽ chống lại việc này bằng cách dùng [CSRF tokens](https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF)_Prevention_Cheat_Sheet). Cookie được đánh dấu là `SameSite` sẽ khộng bị nhìn thấy từ một trang khác.

Nó có hai chế độ: **lax** và **strict**. Chế độ lax cho phép cookie được gửi ở  GET request đầu tiên ( ví dụ khi bạn click link). Strict sẽ không gửi bất cứ cookie của bên thứ 3 nào cả.

### Tôi có nên dùng nó không ?

Bạn hoàn toàn nên thiết lập là `Secure` và `HttpOnly`. Không may là ở thời điểm viết bài thì `SameSite` cookies chỉ có ở  [Chrome và Opera](http://caniuse.com/#search=samesite) nên tạm thời bạn có thể bỏ qua chúng.

### Làm như thế nào ?

|Platform|Tôi cần làm gì ?|
|-|-|
|Rails 4 and 5|Secure và HttpOnly mặc định được bật, đối với SameSite, dùng  [secureheaders](https://github.com/twitter/secureheaders)|
|Django| Các session cookies mặc định là HttpOnly. Chuyển sang secure bằng `SESSION_COOKIE_SECURE = True`. SameSite thì không chắc.|
|Express.js| `cookie: { secure: true, httpOnly: true, sameSite: true }`
|Go|`http.Cookie{Name: "foo", Value: "bar", HttpOnly: true, Secure: true}`, xem thêm về `SameSite` ở  [issue](https://github.com/golang/go/issues/15867).|
|Nginx| Bạn thường sẽ ko set cookie ở Nginx|
|Apache| Bạn thường sẽ ko set cookie ở Apache|

### Tôi muốn biết thêm

- [Cookies - MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies#Secure_and_HttpOnly_cookies)

# Tham khảo
- [https://blog.appcanary.com/2017/http-security-headers.html](https://blog.appcanary.com/2017/http-security-headers.html)
- [Series về XSS của Anh Tranngoc](https://viblo.asia/search?q=author%3AAnh%20Tranngoc%20title%3Axss)
- [What is Reflected XSS?](http://security.stackexchange.com/a/65242)
