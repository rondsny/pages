title: "[svn]如何在linux设置svn忽略列表"
date: 2015-03-17 18:35:20
tags: [svn,linux] 
---


### 管理属性变量的命令 
svn客户端有个属性`ignore` 用于保存忽略的文件或者目录。除此之外，svn其实有好多属性变量用来自定义，如在windows下svn客户端里面属性截图：
![windows svn](/images/301-01.png "windows svn")

但是在linux 下，不可像windows那样有可视化界面进行管理。
执行svn help 命令可以知道有五个命令用于管理svn 属性变量。

    propdel (pdel, pd)                # 删除属性
    propedit (pedit, pe)              # 编辑属性
    propget (pget, pg)                # 获取属性的值
    proplist (plist, pl)              # 列出所有的属性
    propset (pset, ps)                # 设置属性的值

那么有这几个命令，想要编辑`svn:ignore` 变量还不轻而易举。

### 方法1：
首先要给SVN指定默认的编辑器，如下。当然改成其它编辑器也可以。
* `export SVN_EDITOR=/usr/bin/vim` 已经设置的话，可以忽略这一步
* `svn propedit svn:ignore [目录]`

然后可以在vim编辑器中写上需要过滤的目录或者文件。换行隔开，据说空格也可以，但是我没有试过。

### 方法2：
除了propedit可以设置，当然propset 也可以设置。
![svn propset](/images/301-02.png "svn propset")
图片表示将pet目录下的xg_pet.erl文件加入到忽略列表。

### 属性变量文件
在当前目录，有一个`.svn` 目录。当有属性变量的时候，`.svn`目录会生成一个`dir-props`文件用来保存属性变量，如下：
![svn properties file](/images/301-03.png ".svn/dir-props")


### 查看状态
另外说一个linux下很常用的命令。相当于windows下commit的时候出现的文件列表。而linux下需要用`svn status`来查看。
`svn status/svn st/svn stat`

延伸一下，下面两个命令：
* `svn st | grep ^? | sed 's/?    //' | xargs svn add`  增加尚未增加到svn的文件
* `svn st | grep ^! | sed 's/!    //' | xargs svn rm`    删除svn里面已经不存在的文件（本地尚存）

当然避免误操作，我经常先执行`svn st | grep ^? | sed 's/?    //'` 先确认下文件列表。
![svn skill](/images/301-04.png "svn skill")
