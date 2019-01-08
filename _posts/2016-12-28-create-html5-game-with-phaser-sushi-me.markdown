---
layout: post
title:  "Create HTML5 game with Phaser : Sushi Me"
date: 2016-12-28 02:18:00 +0700
categories: game phaserjs
---

# Create HTML5 game with Phaser

## Intro và chém gió

Mình thích làm game (và cả chơi game nữa :D). Mơ ước từ nhỏ vẫn là trở thành một **game developer** và được vào làm việc cho những công ty game lớn như Nintendo, Konami,... (yaoming). Tuy nhiên, khi lớn lên thì mơ ước đó không còn được mạnh mẽ như trước nữa, nhưng mong muốn được tự mình làm game thì vẫn còn và giờ nó là một sở thích nho nhỏ mỗi khi có thời gian rảnh.

Mình đã từng thử lập trình game với nhiều ngôn ngữ khác nhau: **Java**, **Python** (với pygame), Godot,...Lần này, là với **Javascript** (framework **PhaserJS**). Để biết sơ qua về PhaserJS, mình đề nghị bạn đọc bài viết sau [Lập trình game javascript sử dụng Phaser](https://viblo.asia/princebk/posts/XogBG29bMxnL) của tác giả [@princebk
](https://viblo.asia/u/princebk). Đây là một bài viết rất cơ bản khi mới bắt đầu làm quen với PhaserJS. Còn nội dung bài viết này sẽ chỉ nói qua về các bước tổng quan để tạo được một game HTML5 đơn giản. Các hướng dẫn về cài đặt môi trường bạn có thể xem ở bài viết trên nhé :)

## From GreenMe to SushiMe

Để làm quen với game thì có vẻ cách thông thường nhất đấy là clone lại một game khác. Giống như hiện tượng **Flappy Bird**, game này đã trở thành đối tượng clone của không biết bao nhiều người và đã trở thành "Hello Word" của giới làm game. Để clone game này đã có hướng dẫn [How to make a Flappy Bird in HTML5 - Part 1](http://blog.lessmilk.com/how-to-make-flappy-bird-in-html5-1/) cực kỳ hữu ích nên ở đây mình sẽ clone 1 game khác: [GreenMe](https://play.google.com/store/apps/details?id=air.GreenMe)

![green_me.png](https://viblo.asia/uploads/e91cfc41-2a3b-4ad1-88a5-59f030a7e5ee.png)

Get it here: [https://play.google.com/store/apps/details?id=air.GreenMe](https://play.google.com/store/apps/details?id=air.GreenMe)

Được làm bởi [@bs90](https://viblo.asia/u/bs90), GreenMe có luật chơi rất đơn giản:
- Bạn có một bảng 5 x 5 gồm các ô tròn có màu xanh, đỏ, vàng
- Khi click vào một ô tròn thì 8 ô xung quanh sẽ đổi màu theo quy tắc sau: xanh -> đỏ -> vàng rồi lại xanh.
- Nhiệm vụ của bạn là đưa tất cả về màu xanh (nên mới có tên là GreenMe)
- Ban đầu bạn sẽ có sẵn một số điểm, click sẽ trừ điểm, khi qua level sẽ được cộng một số điểm kha khá.
- Liệu bạn có thể đạt được bao nhiêu điểm ?

Quả là một trò chơi thích hợp để giết thời gian đúng ko :D. Mình sẽ sử dụng sushi thay cho các ô và nó như sau:

![sushime.png](https://viblo.asia/uploads/eb1c16e9-ee66-4c7a-8e97-9bab3b2b556d.png)

## Let's start

Đầu tiên là khởi tạo project:

```sh
[vigo@ubuntu ~/lab]$ mkdir sushi_me
[vigo@ubuntu ~/lab]$ cd sushi_me
[vigo@ubuntu ~/lab/sushi_me]$
```

và tạo các file ban đầu

```sh
[vigo@ubuntu ~/lab/sushi_me]$ yo phaser-official

     _-----_
    |       |
    |--(o)--|   .--------------------------.
   `---------´  |    Welcome to Yeoman,    |
    ( _´U`_ )   |   ladies and gentlemen!  |
    /___A___\   '__________________________'
     |  ~  |
   __'.___.'__
 ´   `  |° ´ Y `

You're using the fantastic Phaser generator.
? What is the name of your project? green_me
? Which Phaser version would you like to use? 2.4.3
? Game Display Width 800
? Game Display Height 600
   create Gruntfile.js
   create css/styles.css
   create bower.json
   create config.json
   create package.json
   create index.html
   create game/states/boot.js
   create game/states/preload.js
   create game/states/menu.js
   create game/states/play.js
   create game/states/gameover.js
   create assets/preloader.gif
   create assets/yeoman-logo.png
   create templates/_main.js.tpl
   create game/main.js
   create .bowerrc
   create .gitignore
   create .editorconfig
   create .jshintrc

I'm all done. Running bower install & npm install for you to install the required dependencies. If this fails, try running the command yoursef
```

xong xuôi ta chạy:

```sh
[vigo@ubuntu ~/lab/sushi_me]$ grunt
```

Để chạy server tự động load lại game khi có sự thay đổi. Generator cũng đã tạo sẵn cho ta một game đơn giản để chơi thử.

Tiếp theo là phần coding. Mình sử dụng editor [Brackets](http://brackets.io/) cùng với plugin [Brackets-Ternific](https://github.com/MiguelCastillo/Brackets-Ternific) và [tern-phaser](https://github.com/angelozerr/tern-phaser/) để hỗ trợ auto-complete.

## Source Code

Github: [https://github.com/vigov5/sushi_me](https://github.com/vigov5/sushi_me)

## Game States

Khi khởi tạo, ta đã có sẵn các state của game như sau:

- boot : khởi động game, ta có thể thêm ảnh loading tại đây
- preload : tại state này các assets cần thiết cho game sẽ được load vào cache
- menu : hiện ra menu cho người chơi
- play : chơi game
- gameover : chơi thua sẽ đến state này.

## Preload State

Hãy thay đổi file `game/states/preload.js` như sau:

```javascript

'use strict';
function Preload() {
    this.asset = null;
    this.ready = false;
}

Preload.prototype = {
    preload: function() {
        this.asset = this.add.sprite(this.game.width/2, this.game.height/2, 'preloader');
        this.asset.anchor.setTo(0.5, 0.5);

        this.load.onLoadComplete.addOnce(this.onLoadComplete, this);
        this.load.setPreloadSprite(this.asset);
        // load required assets
        this.load.spritesheet('foods', 'assets/foods.png', 56, 56, 3);
        this.load.bitmapFont('carrier_command', 'assets/carrier_command.png', 'assets/carrier_command.xml');
    },
    create: function() {
        this.asset.cropEnabled = false;
    },
    update: function() {
        if(!!this.ready) {
            this.game.state.start('play');
        }
    },
    onLoadComplete: function() {
        this.ready = true;
    }
};

module.exports = Preload;
```

Ta có thể thấy là mỗi state đều có các function:
- preload: load các assets cần thiết cho state này
- create: được chạy 1 lần khi bước vào state, khởi tạo và thiết lập cấu hình
- update: sẽ được chạy sau một khoảng delta cố định để cập nhật thay đổi

Ở state này ta chỉ có nhiệm vụ load vào các assets cần dùng:
- foods: là hình sushi của game, có 3 loại : sushi, makizushi (sushi cuốn), và onigiri (cơm nắm). mỗi ảnh sẽ có kích thước 56 x 56 (mình tham khảo từ đây [https://www.pinterest.com/pin/372321094172202030/](https://www.pinterest.com/pin/372321094172202030/))
- carrier_command : là font bitmap mình dùng, lấy từ 1 ví dụ trên trang chủ Phaser. Thêm thông tin tại: [http://phaser.io/examples/v2/text/bitmap-fonts](http://phaser.io/examples/v2/text/bitmap-fonts)

Sau khi load xong ta chuyển luôn sang state play `this.game.state.start('play');`

## Play State

Đây là phần nội dung chính của game.

### Create

Ta thiết lập màu nền cho game và mảng 2 chiều `this.grid` để chứa các ô của game. Cùng xem phần khởi tạo:

```javascript
this.grid[i][j] = new Cell(this.game, this.game.width/2 - 60*5/2 + i*60, 150 + j*60, j, i, 0);
this.game.add.existing(this.grid[i][j]);
this.grid[i][j].inputEnabled = true;
this.grid[i][j].events.onInputDown.add(this.clickListener, this);
```

mỗi ô đều là một đối tượng `Cell`, ta thiết lập vị trí hiển thị và vị trí của cell đó trong bảng, chấp nhận click vào cell thông qua `this.grid[i][j].inputEnabled = true;` và định nghĩa hàm callback là `this.clickListener` khi cell bị click vào.

```javascript
clickListener: function(object) {
    this.clickCell(object.row, object.col, true);
},
```

```javascript
clickCell: function(col, row, changeScore){
    for (var i = 0; i < this.deltas.length; i++) {
        var targetCol = col + this.deltas[i][0];
        var targetRow = row + this.deltas[i][1];
        if (targetCol >= 0 && targetCol < 5 && targetRow >= 0 && targetRow < 5) {
            this.grid[targetRow][targetCol].flip();
        }
    }
    if (changeScore) {
        this.score -= 5;
    }
},
```

Tại đây ta kiểm tra xem cell nào nào cell xung quanh của cái bị click và tiến hành `flip()` nó. Cùng xem qua `filp()` ở `game/prefabs/cell.js` nhé:

```javascript
'use strict';

var Cell = function(game, x, y, row, col, frame) {
    Phaser.Sprite.call(this, game, x, y, 'foods', frame);
    this.col = col;
    this.row = row;
    this.game.physics.arcade.enableBody(this);
};

Cell.prototype = Object.create(Phaser.Sprite.prototype);
Cell.prototype.constructor = Cell;

Cell.prototype.update = function() {
    // write your prefab's specific update code here
};

Cell.prototype.flip = function() {
    this.frame = (this.frame + 1) % 3;
}

module.exports = Cell;
```

`this.frame` sẽ chỉ định hình ảnh món ăn nào đang được hiển thị cho ô đó. Thay đổi thuộc tính này sẽ thay đổi món ăn được hiển thị.

### Update

```javascript
update: function() {
    this.scoreText.setText('' + this.score);
    this.scoreText.x = this.game.width / 2 - this.scoreText.textWidth / 2;

    var done = true;
    for (var i = 0; i < 5; i++) {
        for (var j = 0; j < 5; j++) {
            if (this.grid[i][j].frame != 0) {
                done = false;
                break;
            }
        }
    }
    if (done) {
        this.score += this.BASE_SCORE * this.level;
        this.level += 1;
        this.levelText.setText('level:' + this.level);
        this.generateLevel(this.level);
    }
}
```

Kiểm tra toàn bộ các cell, nếu tất cả đều là sushi thì ta sẽ chuyển qua level mới.

```javascript
resetLevel: function() {
    for (var i = 0; i < 5; i++) {
        for (var j = 0; j < 5; j++) {
            this.grid[i][j].frame = 0;
        }
    }
},
generateLevel: function(level) {
    this.resetLevel();
    for (var i = 0; i < level; i++) {
        var col = this.game.rnd.integerInRange(0, 4);
        var row = this.game.rnd.integerInRange(0, 4);
        this.clickCell(row, col, false);
    }
}
```

Trước khi tạo level mới ta đưa toàn bộ các ô về trạng thái ban đầu rồi tiến hành click ngẫu nhiên vào các ô để sinh ra level mới. Easy

Ngoài ra còn các phần xử lý khác liên quan đến bitmap font, bạn có thể xem thêm trong source code nhé :D

## Demo

Game: [http://vigov5.github.io/sushi_me/index.html](http://vigov5.github.io/sushi_me/index.html)

## The End

Việc tạo một game HTML5 với PhaserJS cực kì đơn giản và nhanh do có bộ thư viện rất mạnh mẽ. Mình đã hoàn thành cơ bản game này chỉ trong 1 buổi sáng. Lần tới mình sẽ thử sức với một game khó hơn. See ya !

# References

- <http://phaser.io/>
- <http://brackets.io/>
- <http://blog.lessmilk.com/how-to-make-flappy-bird-in-html5-1/>
- <http://www.codevinsky.com/phaser-tutorial-getting-started-with-generator-phaser-official/>
- <http://www.codevinsky.com/phaser-2-0-tutorial-flappy-bird-part-1/>
- <http://www.creativebloq.com/web-design/how-develop-game-phaser-81516083>
- <http://www.sitepoint.com/javascript-game-programming-using-phaser/>
- <http://www.antonoffplus.com/html5-game-development-bookmarks/>
