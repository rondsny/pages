title: "[linux]CentOS下安装和使用tmux"
date: 2015-04-28 18:27:54
tags: [linux,centos,tmux]
---

前天随意点开博客园，看到了一篇关于tmux的文章 [Tmux - Linux从业者必备利器](http://cenalulu.github.io/linux/tmux/)，特意还点进去看了。毕竟Linux对于做游戏服务端开发的我来说，太熟悉不过了。不过我就粗略地看了一眼，就关掉了。直到第二天`码农周刊`就推荐了这篇文章，才引起我真正的关注。`tmux`真的那么好用吗？所以我自己也倒腾来一遍，的确在许多场景下还是非常有用的。如：

- 做服务器的，肯定需要关注性能的，而tmux多个pane可以很方便同时关注多项性能指标；
- 我们的游戏服刚好有多个服务存在，而联调多个服务的时候，可以同时看到多个控制台确实很方便。

以上并不是其它方式不可以，譬如我用xshell的，同时看多个xshell可以达到相同的效果。但切换的时候还是有些不方便。 因为环境不同，原作者用Mac，而我用CentOS，有些地方存在不一样，故记载方便自己以后查阅。

### CentOS下安装 ###

首先我是用`yum install tmux`尝试安装的。估计没有源，没有找到tmux。所以习惯性直接找源代码安装。
但是其中有依赖，需要先安装`libevent`。

    wget https://github.com/downloads/libevent/libevent/libevent-2.0.21-stable.tar.gz
    tar xzvf libevent-2.0.21-stable.tar.gz
    cd libevent-2.0.21-stable
    ./configure && make
    make install

然后再下载源码安装tmux

    git clone git://git.code.sf.net/p/tmux/tmux-code tmux
    cd tmux
    sh autogen.sh
    ./configure && make
    make install

过程中遇到了两个报错，解决都比较简单，当然是查阅资料后。

#### 问题1： ####
期间我遇到了执行autogen.sh 报错，原因是我没有安装automake。这个直接`yum install automake`就简单解决了。

#### 问题2： ####
执行的时候遇到
	
    libevent-2.0.so.5: cannot open shared object file: No such file or directory

的报错，解决办法也比较简单，既然找不到，那就换个找得到的地方呗。

    ln -s /usr/local/lib/libevent-2.0.so.5 /usr/lib/libevent-2.0.so.5     # 32位系统
    ln -s /usr/local/lib/libevent-2.0.so.5 /usr/lib64/libevent-2.0.so.5   # 64位系统

### 使用和快捷键 ###

直接在命令行输入tmux即可进入tmux的模式。

tmux主要有windows窗体操作和Pane操作，个人觉得windows对于我来说，意义不大(并不是说windows模式没适用场景)，所以这里主要讲下Pane的相关操作。

#### 快捷键 ####

tmux的快捷键都要先按`C-b(Ctrl-b)`。然后再按下面表格内容，才能达到相应的效果。

#### session和其他相关快捷键 ####

 快捷键 |     功能      
:-----:|:-------------
 C-z   | 关闭tmux.
 :     | 进入tmux命令行模式.
 ?     | 列出所有快捷键.
 t     | **显示时间.**
 d     | 退出当前tmux客户端，tmux后台运行.
       | 
 $     | 重命名当前session.
 s     | **切换session 显示所有session并切换到某一个session.**
 (     | 切换session 切换到上一个session.
 )     | 切换session 切换到下一个session.
 L     | 切换session 到前一个活跃的session.

#### window相关快捷键 ####

 快捷键  |     功能      
:------:|:-------------
 c      | **新增一个window.**
 &      | 退出当前window.
 ,      | 重命名当前window.
 l      | 跳转到上一个所在window.
        | 
 i      | 显示当前window的信息.
 w      | **切换window 显示所有window并切换window.**
 0 to 9 | 切换window 到相应编号的window.
 p      | 切换window 上一个window.
 n      | 切换window 下一个window.
 ’      | 切换window 到输入编号的window.
 f      | 切换window 到搜索到的window.
 Space  | 改变当前window下的pane布局.


#### pane相关快捷键 ####

  快捷键               |     功能      
:--------------------:|:-------------
 !                    | **从window移除当前pane.**
 "                    | **将当前pane变成上下两个pane.**
 %                    | **将当前pane变成左右两个pane.**
 x                    | **关闭当前pane.**
 q                    | 显示pane的索引.
 z                    | **最大化或者恢复当前pane.**
 {                    | 跟前一个pane交换位置.
 }                    | 跟后一个pane交换位置.
 o                    | 切换Pane 到下一个pane.
 ;                    | **切换Pane 进入到前一个操作过的pane.**
 Up, Down Left, Right | 切换Pane 使用方向键切换到相应方向的pane.

可能有些快捷键有些出入，可以的话提醒下。另外有些快捷键没有搞懂，而且快捷键比较多，个人觉得记得主要的几个切换快捷键就足够用来。比较tmux只是一个协助工具，没有必要在其上面那么用心。加粗的是个人觉得比较实用的。

tmux不中断session的模式确实很666666，每次连回去就可以快速接上上次结束的环境。而且多个pane也非常适合要开启并监控多个服务的情况。

![多个pane例子](http://i.imgur.com/guRsWo3.png)

### 参考资料 ###


1. [http://cenalulu.github.io/linux/tmux/](http://cenalulu.github.io/linux/tmux/ "Tmux - Linux从业者必备利器")
2. [http://elroyjetson.org/dev-notes/centos/installing-tmux-on-centos-6-2](http://elroyjetson.org/dev-notes/centos/installing-tmux-on-centos-6-2 "Installing tmux on CentOS 6.2")
3. [http://www.nigeldunn.com/2011/12/11/libevent-2-0-so-5-cannot-open-shared-object-file-no-such-file-or-directory/](http://www.nigeldunn.com/2011/12/11/libevent-2-0-so-5-cannot-open-shared-object-file-no-such-file-or-directory/ "libevent-2.0.so.5: cannot open shared object file: No such file or directory")