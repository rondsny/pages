title: "[windows]快速从ftp下载最新软件包的批处理脚本 "
date: 2015-11-14 17:15:57
tags: windows
---

### 背景

由于敏捷开发，快速迭代，我们项目一天会有三个版本，也就意味着我一天要去获取三次软件包。我负责服务端开发，所以我经常需要去拿最新的客户端。我们的客户端放置在一个公共的ftp上面。每天频繁登陆ftp下载，或者使用ftp工具，每次都要点击同步，都不太方便。如果在linux下就好了，然而在windows也是可以运行脚本的，何不尝试下呢。

### 完整代码

    @echo off
    rem for download file
    rem ftp config 
    rem ip login_name password remote_dir
    
    set "ftp_ip=192.168.0.1"
    set "ftp_user=admin"
    set "ftp_pass=123456"
    set "ftp_path=/"
    
    set "f_tmp=tmp"
    set "f_info=tmp\tmp_info.dat"
    set "f_list=tmp\tmp_list.dat"
    
    rd /s /q pack
    mkdir %f_tmp%
    
    echo open %ftp_ip% > %f_info%
    echo user %ftp_user% >> %f_info%
    echo %ftp_pass%>> %f_info%
    echo prompt >> %f_info%
    echo binary >> %f_info%
    echo cd %ftp_path% >> %f_info%
    echo ls . %f_list% >> %f_info%
    echo lcd %f_tmp% >> %f_info%
    echo disconnect >> %f_info%
    echo bye >> %f_info%
    
    ftp -v -n -s:%f_info%
    
    
    for /f "delims=" %%i in ('type "%f_list%"') do (
        set "target_7z=%%i"
    )
    
    echo open %ftp_ip% > %f_info%
    echo user %ftp_user% >> %f_info%
    echo %ftp_pass%>> %f_info%
    echo prompt >> %f_info%
    echo binary >> %f_info%
    echo cd %ftp_path% >> %f_info%
    echo lcd %f_tmp% >> %f_info%
    echo get %target_7z%>> %f_info%
    echo disconnect >> %f_info%
    echo bye >> %f_info%
    
    ftp -v -n -s:%f_info%
    
    call tools\7z\x64\7za.exe x %f_tmp%\%target_7z%
    
    rd /s /q %f_tmp%
    
    exit

![运行脚本](http://7xaw5u.com1.z0.glb.clouddn.com/windowsQQ截图20151114170729.png)

### 逐步解释

#### 获取文件列表

    echo open %ftp_ip% > %f_info%
    echo user %ftp_user% >> %f_info%
    echo %ftp_pass%>> %f_info%
    echo prompt >> %f_info%
    echo binary >> %f_info%
    echo cd %ftp_path% >> %f_info%
    echo ls . %f_list% >> %f_info%
    echo lcd %f_tmp% >> %f_info%
    echo disconnect >> %f_info%
    echo bye >> %f_info%
    
    ftp -v -n -s:%f_info%

这部分代码主要有以下几个作用：
1. 将ftp的命令写入到文件；
2. 在ftp上获取对应目录的文件列表，并写到本地文件下。

#### 获取最新的一个文件

    for /f "delims=" %%i in ('type "%f_list%"') do (
        set "target_7z=%%i"
    )

然后循环遍历文件列表，最终获取到最后一个列表（也就是最新的文件名）。

#### 下载最新文件

    echo open %ftp_ip% > %f_info%
    echo user %ftp_user% >> %f_info%
    echo %ftp_pass%>> %f_info%
    echo prompt >> %f_info%
    echo binary >> %f_info%
    echo cd %ftp_path% >> %f_info%
    echo lcd %f_tmp% >> %f_info%
    echo get %target_7z%>> %f_info%
    echo disconnect >> %f_info%
    echo bye >> %f_info%
    
    ftp -v -n -s:%f_info%

有了文件名，我们就可以再执行一次ftp命令，下载我们最新的文件了。以上就实现了动态下载最新文件了。

#### 解压

这边我们使用的软件包是7z打包的。所以也要下载7z解压工具。
官方地址：http://www.7-zip.org/
然后下载到命令行版，放置到任意可读取目录就可以了。

    call tools\7z\x64\7za.exe x %f_tmp%\%target_7z%

### 后话

平常习惯了在linux下倒腾。可以写些脚本做些繁琐的事情，但是在windows经常就傻眼了。可视化的东西是有很多好处，但是也有些弊端。批处理脚本虽然不好用，但也并不是不可用。很多时候也可以带来很大的方便。当然会python、ruby这些脚本语言其实也是完全可以满足的。毕竟现在这年头批处理这种东西用的越来越少了。`windows shell`也可以，但是感觉也不太好用。

### 参考资料

- http://occool.com/2012/03/【转载】命令行压缩解压7z/
- http://www.robvanderwoude.com/ftp.php