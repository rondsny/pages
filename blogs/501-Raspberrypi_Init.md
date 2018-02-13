title: "[linux]树莓派入手体验和系统安装"
date: 2015-11-05 20:00:00
tags: [linux, respberrypi]
---

![树莓派](http://i.imgur.com/iAoxxbE.png)

### 背景

一直想捣鼓点什么东西。当看到树莓派的时候，就是它了。

树莓派可以安装`Linux`系统，而我在工作当中，可以说`Linux`是一半工作环境。树莓派真是个好东西，这个东西应该在我学习`linxu/Unix`的时候就该接触了。想想大学的时候，在`windows`下安装虚拟机，安装`Linux`是件多么痛苦的事情。而且那时的电脑配置也不算高，才2G内存，还要开虚拟机。玩个蛋蛋。

对`Linux`也算比较熟吧，入手一个树莓派应该可以玩很多好玩的事情。

### 购买硬件

直接在某宝搜索入手。必须内容：

- 树莓派一个（`Raspberry Pi 2`）
- 小usb口电源（5V2A的充电器随便找一个）
- 4G或者更大存储空间的SD卡一张（树莓派本身不带存储空间）

以下非必需： 

- 散热器三片（风扇什么的觉得也太夸张了）
- 无线网卡（本身有网卡入口，所以不是必须的）
- SD卡读卡器（安装系统的时候会用到）

![树莓派连接外置硬件](http://i.imgur.com/0LQEdsC.jpg)

### 安装系统

树莓派得到了各种`Linux`发行版本的支持，甚至微软在自己的`windows 10`上也发行了一个支持树莓派的版本。最常见的，还是在树莓派上面安装`RASPBIAN`和`Ubuntu`。`RASPBIAN`是树莓派官方出品基于`Debian`的`Linux`系统。也有喜欢在树莓派上面玩`windows 10`的。相关的系统官方都有提供下载。（[https://www.raspberrypi.org/downloads/](https://www.raspberrypi.org/downloads/ "https://www.raspberrypi.org/downloads/")）。

我本人安装的是官方提供的`RASPBIAN`系统，基于`Debian`实现。可以说对`Debian`比较了解，所以`RASPBIAN`对我来说是一个比较好的选择。以安装`RASPBIAN`为例，有多种安装方式。

树莓派官方推荐的是使用其官方工具`NOOBS`安装工具。

1. 下载`NOOBS`工具（[https://www.raspberrypi.org/downloads/noobs/](https://www.raspberrypi.org/downloads/noobs/ "https://www.raspberrypi.org/downloads/noobs/")）；
2. 下载SD卡格式化工具（[https://www.sdcard.org/downloads/formatter_4/eula_windows/](https://www.sdcard.org/downloads/formatter_4/eula_windows/)）；
    1. 安装SD卡格式工具；
    2. 在选项Option里面设置“FORMAT SIZE ADJUSTMENT”为开启ON状态；
    3. 检查SD卡是否插入电脑；
    4. 点击格式化工具的【格式化(Format)】按钮格式化SD卡。
3. 解压NOOBS.zip文件；
4. 将解压的文件复制到SD卡上面；
5. 将SD卡插入到树莓派里面；
6. 接上鼠标、键盘、显示器（这一部非必需）；
7. 接上网线（无线网卡也可以）、电源，然后就自动开机启动了。

开机启动后，树莓派会自行安装系统，看sd卡的写的速度时间会不一样，10~60分钟估计就好了。然后就会进入了树莓派的系统界面。至此，算是大功告成了。
![安装系统](http://i.imgur.com/pHuni3O.jpg)


#### 关于系统
树莓派官方系统`RASPBIAN`是基于`Debian`修改而来的。所以熟悉`Debian`和`Ubuntu`的话，对`RASPBIAN`是完全没有任何入门门槛的。`RASPBIAN`使用的是树莓派自己的镜像。其服务器在国外，访问起来可能有速度慢的情况，建议修改成网易的`Debian`镜像(http://mirrors.163.com/.help/debian.html)。
编辑/etc/apt/sources.list文件, 在文件最前面添加以下条目(操作前请做好相应备份)

    deb http://mirrors.163.com/debian/ wheezy main non-free contrib
    deb http://mirrors.163.com/debian/ wheezy-updates main non-free contrib
    deb http://mirrors.163.com/debian/ wheezy-backports main non-free contrib
    deb-src http://mirrors.163.com/debian/ wheezy main non-free contrib
    deb-src http://mirrors.163.com/debian/ wheezy-updates main non-free contrib
    deb-src http://mirrors.163.com/debian/ wheezy-backports main non-free contrib
    deb http://mirrors.163.com/debian-security/ wheezy/updates main non-free contrib
    deb-src http://mirrors.163.com/debian-security/ wheezy/updates main non-free contrib

执行`sudo apt-get update`更新软件包列表。详细可以查看网易`Debian`镜像的使用帮助（http://mirrors.163.com/.help/debian.html）。

### 结束语
树莓派最大的优势在于便宜，而且资料方面也算比较充足。个人觉得最大的价值还是拿来学习Linux的知识。独立的Linux机器，比起虚拟机，给人带来的学习积极性和成就感感觉是完全不一样的。当然，在可玩性方面，树莓派也可以做很多有趣的事情。倒腾飞行器、遥控玩具车、控制家庭电器、控制门禁、制作超级电脑等等。最主要的还是要有兴趣。而我，是想让树莓派来实现一些没有必要使用PC、需要长时间、或者定期任务的执行。

### 参考资料
- http://mirrors.163.com/.help/debian.html
- https://www.raspberrypi.org/help/quick-start-guide/