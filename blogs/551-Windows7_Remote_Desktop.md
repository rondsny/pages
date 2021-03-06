title: "[windos]Windows7远程桌面连接"
date: 2018-2-13 15:40:26 
tags: windows
---

# Windows7远程桌面连接

## 1. 简要步骤

	1. 设置被远程目标机器的访问权限；
		1.1. 设置目标机器密码；
		1.2. 设置允许被远程连接；
		1.3. 获取目标机器的ip。
	2. 发起远程。

## 2. 详细说明

### 2.1. 设置被远程机器的访问权限

#### 2.1.1. 设置机器密码

因为远程连接必须要求使用用户名密码登录，主要是为了安全。如果你的电脑已经设置了密码，可以直接跳过。

如果没有设置密码，可以在`[控制面板-用户账户和家庭安全]`面板进入设置。
![](/pics/rpc_005.png)

#### 2.1.2. 设置允许被远程连接

Windows默认设置是不允许被远程连接的。所以我们要把远程连接的开关开启起来。

打开`[控制面板]`，进入`[控制面板-系统和安全-系统]`面板。也可以如下图方式打开

![](/pics/rpc_000.png)
![](https://raw.githubusercontent.com/rondsny/pages/master/blogs/pics/rpc_000.png)

点击面板中的`[远程设置]`按钮（如下图），进入系统设置。如图勾选【仅允许运行使用网络级别身份验证...】，点击【确认】成功设置。

![](/pics/rpc_001.png)
![](https://raw.githubusercontent.com/rondsny/pages/master/blogs/pics/rpc_001.png)

#### 2.1.3. 获取被远程机器的ip

途径有很多，最快捷的就是点【开始】然后输入cmd，直接快捷打开cmd面板。然后在面板输入`ipconfig`查看ipv4的地址，如下图。

![](/pics/rpc_003.png)
![](https://raw.githubusercontent.com/rondsny/pages/master/blogs/pics/rpc_003.png)

### 2.2. 发起远程

在另外一台电脑上面，点击【开始-附件-远程桌面连接】（如下图），打开远程功能面板。

![](/pics/rpc_002.png)
![](https://raw.githubusercontent.com/rondsny/pages/master/blogs/pics/rpc_002.png)

在面板输入被远程机器的ip地址，然后输入用户名称密码（后面会弹出输入密码提示），即可远程访问到另外一台机器。

![](/pics/rpc_004.png)
![](https://raw.githubusercontent.com/rondsny/pages/master/blogs/pics/rpc_004.png)

## 3. 其他

win10的设置和访问步骤基本类似。