---
layout: post
title:  "Create a private blockchain based on Ethereum platform"
date: 2017-12-24 15:39:00 +0700
categories: blockchain ethereum
---

X-post: [https://viblo.asia/p/tu-thiet-lap-private-blockchain-dua-tren-nen-tang-ethereum-RQqKLg0457z](https://viblo.asia/p/tu-thiet-lap-private-blockchain-dua-tren-nen-tang-ethereum-RQqKLg0457z)

![](https://viblo.asia/uploads/03610578-38ae-43be-9cce-f0e47b5bb15d.jpeg)
# Giới thiệu

Gần đây thì Bitcoin, công nghệ blockchain, Ethereum, smart contract đã trở thành chủ đề trên rất nhiều các diễn đàn cũng như các trang báo, và bạn bắt đầu tự hỏi chúng là gì, có gì hay ho mà nhiều người chú ý đến như vậy.
Với mình, thay vì lý thuyết khô khan, tôi thích đi vào tìm hiểu hands-on trước, sau đó mới quay lại đọc lý thuyết :sweat_smile:. Bởi vậy trong bài này, mình muốn chia sẻ cách thiết lập một private blockchain trên nền tảng Ethereum qua những gì mình tìm hiểu được, xây dựng môi trường để ta có thể phát triển các smart contract sau này :ok_hand:

<!--description-->

# Thiết lập private blockchain

## Cài đặt Geth

[Geth](https://geth.ethereum.org/downloads/) là client giúp chúng ta có thể giao tiếp với mạng lưới Ethereum blockchain, thực hiện các giao dịch, smart contract, mining. Bạn có thể ghé qua trang chủ để chọn phiên bản phù hợp với hệ điều hành mà mình đang dùng. Mình dùng Mac OS X nên sẽ cài đặt bằng **Homebrew**

```
brew tap ethereum/ethereum
brew install ethereum
```

Với Ubuntu/Linux

```
sudo apt-get install software-properties-common
sudo add-apt-repository -y ppa:thereum/ethereum
sudo apt-get update
sudo apt-get install ethereum
```

## Tạo tài khoản miner

Miner là những thợ đào ở trong hệ thống. Họ là những người sử dụng năng lực tính toán của máy tính để tìm ra những block mới thỏa mãn độ khó mà hệ thống yêu cầu, giúp cho giao dịch được xác nhận và hệ thống tiếp tục tiếp diễn. Không có miner thì hệ thống blockchain sẽ không thể hoạt động được. Đổi lại cho công sức đã bỏ ra, miner sẽ nhận được phần phí giao dịch như là phần thưởng cho mình.

Chúng ta sẽ cần tạo một tài khoản miner để làm thợ mỏ chính trong private blockchain. Một account sẽ gồm một cặp public/private key và password dùng để bảo vệ cho private key. Bạn có thể hiểu nó khá tương đương với những thuật ngữ khi chúng ta sử dụng khóa cho SSH chẳng hạn.
- **Public key**: Là thứ được công khai trên hệ thống blockchain, từ public key có thể sinh ra địa chỉ ví ethereum, thứ định danh cho các account trên hệ thống
- **Private key**: khóa bí mật, dùng để ký (sign) những giao dịch được sinh ra từ tài khoản này. Về cơ bản, ta sẽ ký, mã hóa giao dịch bằng private key, đưa lên trên hệ thống, hệ thống có thể dùng public key được công khai để xác thực rằng giao dịch đó được thực hiện bởi ta chứ không phải 1 ai khác.

Tất cả dữ liệu của *geth* đều được chứa trong thư mục **datadir**. Trong bài này mình sẽ sử dụng thư mục: `~/lab/ethereum_viblo`. Thư mục mặc định của các hệ điều hành khác như sau:

- Mac: `~/Library/Ethereum`
- Linux: `~/.ethereum`
- Windows: `%APPDATA%\Ethereum`

Vì chúng ta thiết lập private blockchain nên tất cả các lệnh chúng ta sẽ cần chỉ định **datadir** như trên.

```
[nguyen.anh.tien@TienNA ~]$ geth account new --datadir ~/lab/ethereum_viblo/
Your new account is locked with a password. Please give a password. Do not forget this password.
Passphrase: 
Repeat passphrase: 
Address: {646cb67fa5f121e4ed674d9dbef8f1b177f20c3f}
```

Chú ý: **KHÔNG ĐƯỢC QUÊN PASSWORD** nhé.

OK, vậy là ta đã có địa chỉ ví cho miner để có thể nhận được thưởng khi đào block mới.

## Tạo genesis block (block khởi thủy)

Mỗi blockchain đều được bắt đầu bởi 1 block đặc biệt gọi là `genesis block` (tạm gọi là block khởi thủy). Các block tiếp theo sẽ được xây dựng trên block khởi thủy và  cứ block sau sẽ tham chiếu đến block trước (cụ thể là tính toán/lưu hash của block trước). Đối với Ethereum, block khởi thủy được sinh ra vào ngày 20/07/2015. Còn chúng ta sẽ tạo block khởi thủy mới cho private blockchain của mình như sau (feel like a GOD)

```
geth -datadir ~/lab/ethereum_viblo/ init ~/lab/ethereum_viblo/sample_genesis.json
```

với `sample_genesis.json` có nội dung như sau:

```
{
    "config": {
        "chainId": 22,
        "homesteadBlock": 0,
        "eip155Block": 0,
        "eip158Block": 0
    },
    "difficulty": "0x400",
    "gasLimit": "0x2100000",
    "alloc": {
        "646cb67fa5f121e4ed674d9dbef8f1b177f20c3f": 
         { "balance": "0x1337000000000000000000" }     
    }
}
```

Cụ thể từng mục config như sau:
- **chainid**: id của blockchain của chúng ta. Ethereum không chỉ bao gồm 1 hệ thống blockchain duy nhất mà thực tế là có rất nhiều các network khác nhau. Hệ thống blockchain đang chạy thực tế có tên là `Mainnet` (chainid là 1), các network khác dành cho các mạng test trước khi lên production hoặc các mạng dành cho các phiên bản khác nhau của ethereum sẽ có các chainid khác, ví dụ: morden /expanse mainnet (2), ropsten (3), rinkeby (4), rootstock mainnet (30), rootstock testnet (31), kovan (42), ethereum classic mainnet (61), ethereum classic testnet (62). Private chain mặc định sẽ có id là `1337` theo khuyến cáo của [EIP 155](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-155.md). Chúng ta chọn id = 22, không nằm trong bất cứ chain nào ở trên.
- **homesteadBlock**: bằng 0 nghĩa là chúng ta đang sử dụng phiên bản `homestead` của ethereum. Gần đây thì Ethereum đã nâng câp lên phiên bản `byzantium` vào ngày 16/10/2017.
- **eip155Block**: bằng 0 nghĩa là chain chúng ta sẽ hỗ trợ EIP 155, tập hợp các định nghĩa giao thức, client API, các tiêu chuẩn dành cho smart contract.
- **eip158Block**: tương tự như trên
- **difficulty**: độ khó của chain, giá trị này sẽ ảnh hưởng đến *block time*, khoảng thời gian trung bình cần thiết để một block mới được sinh ra. Chú ý là một khi đã chạy blockchain rồi thì sẽ không thay đổi được giá trị này nữa. Trong ví dụ của chúng ta thì độ khó được thiết lập rất dễ nên với 1 máy tính cấu hình bình thường và 1 thợ mỏ duy nhất là đủ để vận hành cả hệ thống rồi. Cụ thể về công thức tính toán đang được sử dụng cho Ethereum bạn có thể tham khảo [blog](https://medium.facilelogin.com/the-mystery-behind-block-time-63351e35603a) này.
- **gasLimit**: gas là giá nội bộ dùng để chạy các giao dịch hoặc hợp đồng trên Ethereum. Mỗi lệnh tính toán sẽ được gửi đến EVM (Ethereum Virtual Machine) và để chạy 1 lệnh cụ thể sẽ tiêu tốn một số lượng gas tương ứng. Nếu số gas mà người thực hiện không cung cấp đủ thì khi chạy đến giữa chừng, hợp đồng/giao dịch đó sẽ bị thất bại và số gas đã tiêu tốn sẽ bị lãng phí. Khi thực hiện giao dịch, bạn sẽ chỉ định *gasLimit*. Số gas tối đa mà bạn muốn trả để thực hiện giao dịch đó. Còn ở đây, ta chỉ định tổng số *gasLimit* của tất cả giao dịch ở trong block.
- **alloc**: Thiết lập này cho phép nạp sẵn Ether cho một số tài khoản định trước. Ở đây ta sẽ nạp sẵn tài khoản miner của chúng ta với 1 số lượng lớn Ether.

```
[nguyen.anh.tien@TienNA ~]$ geth -datadir ~/lab/ethereum_viblo/ init ~/lab/ethereum_viblo/sample_genesis.json
INFO [12-24|14:00:11] Allocated cache and file handles         database=/Users/nguyen.anh.tien/lab/ethereum_viblo/geth/chaindata cache=16 handles=16
INFO [12-24|14:00:11] Writing custom genesis block 
INFO [12-24|14:00:11] Successfully wrote genesis state         database=chaindata                                                hash=28c28d…f61fe8
INFO [12-24|14:00:11] Allocated cache and file handles         database=/Users/nguyen.anh.tien/lab/ethereum_viblo/geth/lightchaindata cache=16 handles=16
INFO [12-24|14:00:11] Writing custom genesis block 
INFO [12-24|14:00:11] Successfully wrote genesis state         database=lightchaindata
```

Done, giờ chúng ta có thể băt đầu tiến hành mining được rồi

```
geth --mine --rpc --networkid 22 --datadir ~/lab/ethereum_viblo
```

Chú ý thiết lập networkid là 22 là network của chúng ta.
- **--mine**: Chạy mining. Nghĩa là process này sẽ đóng vai trò là một node và là thợ mỏ đào các block mới.
```
INFO [12-24|14:00:47] IPC endpoint opened: /Users/nguyen.anh.tien/lab/ethereum_viblo/geth.ipc 
INFO [12-24|14:00:47] HTTP endpoint opened: http://127.0.0.1:8545 
INFO [12-24|14:00:47] Transaction pool price threshold updated price=18000000000
INFO [12-24|14:00:47] Starting mining operation 
INFO [12-24|14:00:47] Commit new mining work                   number=1 txs=0 uncles=0 elapsed=162.215µs
INFO [12-24|14:00:47] Mapped network port                      proto=udp extport=30303 intport=30303 interface="UPNP IGDv1-IP1"
INFO [12-24|14:00:47] Mapped network port                      proto=tcp extport=30303 intport=30303 interface="UPNP IGDv1-IP1"
INFO [12-24|14:00:51] Successfully sealed new block            number=1 hash=b92000…e97356
INFO [12-24|14:00:51] 🔨 mined potential block                  number=1 hash=b92000…e97356
INFO [12-24|14:00:51] Commit new mining work                   number=2 txs=0 uncles=0 elapsed=1.161ms
INFO [12-24|14:00:52] Successfully sealed new block            number=2 hash=3f8c39…176a1f
INFO [12-24|14:00:52] 🔨 mined potential block                  number=2 hash=3f8c39…176a1f
INFO [12-24|14:00:52] Commit new mining work                   number=3 txs=0 uncles=0 elapsed=118.542µs
```
- **rpc**: Bật HTTP-RPC server. RPC (remote procedure call) đúng như tên gọi của nó, cho phép các client kết nối đến node này tại địa chỉ `http://127.0.0.1:8545 ` để giao tiếp với private blockchain của chúng ta (cụ thể thêm ở phần sau)
- Ngoài ra còn có các tham số khác như `rpcaddr` (địa chỉ host của RPC server), `rpcport` (port của RPC server, mặc định là 8545), `rpccorsdomain` (cho phép các trang solidity editor kết nối đến RPC của chúng ta, ví dụ để chấp nhận tất cả chúng ta có thể thêm `--rpccorsdomain "*"`)

## Chạy console trên Geth

Geth cho phép chúng ta attach một console vào node để có thể tương tác với node thông qua các lệnh. Ví dụ như sau:

```
geth --datadir ~/lab/ethereum_viblo attach ipc:/Users/nguyen.anh.tien/lab/ethereum_viblo/geth.ipc
```

Ta có thể xem danh sách tài khoản cũng như lấy thông tin tài khoản đó. Ví dụ:

```
[nguyen.anh.tien@TienNA ~/lab/ethereum_viblo]$ geth --datadir ~/lab/ethereum_viblo attach ipc:/Users/nguyen.anh.tien/lab/ethereum_viblo/geth.ipc
Welcome to the Geth JavaScript console!

instance: Geth/v1.7.3-stable/darwin-amd64/go1.9.2
coinbase: 0x646cb67fa5f121e4ed674d9dbef8f1b177f20c3f
at block: 506 (Sun, 24 Dec 2017 14:11:06 +07)
 datadir: /Users/nguyen.anh.tien/lab/ethereum_viblo
 modules: admin:1.0 debug:1.0 eth:1.0 miner:1.0 net:1.0 personal:1.0 rpc:1.0 txpool:1.0 web3:1.0

> eth.accounts
["0x646cb67fa5f121e4ed674d9dbef8f1b177f20c3f"]
> eth.getBalance("0x646cb67fa5f121e4ed674d9dbef8f1b177f20c3f")
2.3232355729235784806170624e+25 
```

# Sử dụng ví Ethereum Wallet trên desktop

Thật may cho chúng ta là Ethereum đã có giao diện ví cho các hệ điều hành nên chúng ta không cần thao tác qua dòng lệnh nữa. Bạn có thể tải về từ [đây](https://github.com/ethereum/mist/releases) và cài đặt.
Khi chạy, như thông thường ta sẽ cần chỉ định networkid mà ví cần kết nối đến để có thể sử dụng trên private blockchain của chúng ta. Với Mac OSX, cài đặt mặc định thì bạn chạy như sau:

```
/Applications/Ethereum\ Wallet.app/Contents/MacOS/Ethereum\ Wallet --rpc ~/lab/ethereum_viblo/geth.ipc 
```

Giao diện:

![](https://viblo.asia/uploads/8e476b08-5922-4026-8d36-87ce90f72d76.png)

Như ta thấy, hiện có duy nhất 1 tài khoản Miner trong ví của chúng ta, và vì nó đang mining nên tài khoản thỉnh thoảng lại tăng 1 chút, hihi.

![](https://viblo.asia/uploads/full/6e1bd42a-b816-4eee-95ed-95db04c9c67a.gif)

### Thực hiện giao dịch

Hãy tạo thêm 1 tài khoản mới, đặt tên là `Primary`, và chuyển `100,000 ETH` cho account này. Sử dụng *Add account*, điền mật khẩu cho private key của account mới:
![](https://viblo.asia/uploads/fb3954cd-070f-48a4-bce5-164677302118.png)

Thực hiện giao dịch cũng tương tự, hoàn toàn dễ dàng với giao diện của Ethereum Wallet:

![](https://viblo.asia/uploads/ee131ece-2f5c-4a0e-9f0f-0bf2a66d149d.png)

Bạn có thể thấy là ta có thể thay đổi phí giao dịch, trả nhiều phí hơn thì sẽ được ưu tiên xử lý nhanh hơn. Điền password cho private key để tiến hành giao dịch.

![](https://viblo.asia/uploads/full/c670010d-389c-46b9-b833-e978993a9c94.gif)

Bạn có thể thấy có số *Confirmation* là số xác nhận của miner cho giao dịch của bạn, thông thường hệ thống sẽ cần 2 confirmation để giao dịch có hiệu lực. Vậy là giao dịch thành công :fist:. Check lại phía bên console của miner.

```
INFO [12-24|14:36:43] 🔨 mined potential block                  number=1528 hash=cc63dc…fe8bf7
INFO [12-24|14:36:43] Commit new mining work                   number=1529 txs=0 uncles=0 elapsed=264.992µs
INFO [12-24|14:36:44] Submitted transaction                    fullhash=0xa434de87ebb268ecaafa993476bb3e9810310e756b114f23817dc59db3e09d17 recipient=0xadF5D014d795606C64BD18fb286D4095a6248e22
INFO [12-24|14:36:45] Successfully sealed new block            number=1529 hash=d2581f…84158d
INFO [12-24|14:36:45] 🔗 block reached canonical chain          number=1524 hash=327eab…d9b130
INFO [12-24|14:36:45] 🔨 mined potential block                  number=1529 hash=d2581f…84158d
INFO [12-24|14:36:45] Commit new mining work                   number=1530 txs=1 uncles=0 elapsed=1.842ms
```

# Sử dụng ví MetaMask trên trình duyệt

**MetaMask** là một loại ví Ethereum chạy trên trình duyệt web như là một Chrome extension. Nó sẽ nhúng ethereum web3 API vào tất cả javascript ở trên trang web, thông qua đó các apps có thể tương tác với blockchain.
MetaMask cũng cho phép người dùng tạo tài khoản do vậy, họ có thể xem được các giao dịch sắp diễn ra và có thể chấp nhận thực hiện hoặc từ chối các giao dịch đó.

## Cài đặt

- Tải về từ Chrome Web Store: https://chrome.google.com/webstore/detail/metamask/nkbihfbeogaeaoehlefnkodbefgpgknn
- Thiết lập ban đầu, MetaMask sẽ yêu cầu chúng ta tạo mật khẩu để truy cập ví, cùng với đó là danh sách các seed words để backup trong trường hợp chúng ta quên mật khẩu. Hãy chú ý lưu trữ 2 thông tin này thật cẩn thận.
- Trong danh sách, chọn Localhost 8545 là private network của chúng ta. Chú ý là trước đó bạn cần chạy miner với switch `--rpccorsdomain "*" --rpcapi "web3,eth,net"` để MetaMask có thể kết nối được.

![](https://viblo.asia/uploads/a4cd4484-833b-43d3-b5e6-d3ed4d020c25.png)

## Tạo tài khoản

Xong xuôi ta có thể tạo tài khoản mới. Ở đây mình tạo 2 tài khoản lần lượt có địa chỉ như sau:
- MetaMask 1: 0xd45B8846cAB7c9aEf15D5f9Cc0aac281d9A42117
- MetaMask 2: 0xE65Dc3305a26d91bc8FfAEd0db6f65DA3b1906C2

Ta có thể thử chuyển ETH từ tài khoản Miner dùng Ethereum Wallet cho desktop vào 2 tài khoản này, VD 200,000 ETH vào MetaMask 1, và 400,000 vào MetaMask 2. Kết quả:

![](https://viblo.asia/uploads/7c48327f-295b-4be3-b698-9bb61134c5d5.png)

Và chuyển 100 ETH từ MetaMask 2 sang tài khoải MetaMask 1.

![](https://viblo.asia/uploads/f46306fb-c212-41c6-ba17-c2ddca0e1e79.png)

## Import ví vào Ethereum Wallet

Để có thể sử dụng 2 tài khoản này trên ví Ethereum Wallet desktop, ta cần export private key từ trình duyệt và import vào trong keystore của Geth. VD, private key của MetaMask 2 là:

```
91c10cf66c99909e08074860471b5068ecb3dbbe90d88d7e3f4fe25ff5c91028
```

Ta tạo 1 file `metamask2_private.key` với nội dung trên rồi import như sau:

```
[nguyen.anh.tien@TienNA ~/lab/ethereum_viblo]$ geth account import metamask2_private.key -datadir ~/lab/ethereum_viblo/
Your new account is locked with a password. Please give a password. Do not forget this password.
Passphrase: 
Repeat passphrase: 
Address: {e65dc3305a26d91bc8ffaed0db6f65da3b1906c2}
```

Hai địa chỉ ví trùng nhau, như vậy là ok. Mở ví Ethereum Wallet lên ta sẽ thấy có 1 account 3 được thêm vào với địa chỉ ví của MetaMask 2.

# Cài đặt Blockchain Explorer
Để có thể xem được chi tiết các giao dịch thì Ethereum có [Etherscan](https://etherscan.io) còn đối với private chain như của chúng ta, ta sẽ dùng [Ethereum block explorer](https://github.com/carsenk/explorer) tuy không nhiều tính năng bằng nhưng vẫn khá hữu ích

```
git clone https://github.com/carsenk/explorer
npm install
npm start
```

Truy cập trang thông qua `http://localhost:8000/`:
![](https://viblo.asia/uploads/a16b9acb-452c-4b10-a490-f358b610cef6.png)

Kiểm tra tài khoản:

![](https://viblo.asia/uploads/4dd5dace-319c-4510-8786-0e1ba27750c0.png)


# Kết luận

Chúng ta đã thiết lập thành công private blockchain trên localhost, tiến hành một số giao dịch cơ bản. Ở các bài sau ta sẽ tìm hiểu thêm về Ethereum, cơ chế hoạt động, Solidity, smart contract, cách phát hành token của chính mình. Stay tune !

# Tham khảo
- https://medium.facilelogin.com/build-your-own-blockchain-b8eaeea2f891
- https://medium.facilelogin.com/the-mystery-behind-block-time-63351e35603a
- https://blog.ethereum.org/2015/12/03/how-to-build-your-own-cryptocurrency/
