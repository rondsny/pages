title: "[linux]windows无法访问samba的安全性问题(关闭selinux)"
date: 2015-04-07 18:00:00
tags: [samba,selinux,linux]
---

#### 背景

在某一天重启了虚拟机的 `linux` 之后，我的 `windows` 在连接上 `samba` 之后，点击某些文件夹的时候，会出现没有权限打开的情况。这问题折腾了我一度重新配置了好几次 `samba` 的配置，然而无果。

#### 解决

经过搜索，发现有两个办法可以解决samba的某些文件夹无法访问的问题。

- 方法一 修改文件和文件夹的安全策略；
- 方法二 关闭 `selinux`；

第一种方法并不合适，只是临时解决的一种方案。因为在 `windows` 下新建了一个 `linux` 文件夹之后，下一次重启了 `linux` ，新的文件夹又无法访问了。麻烦。第二种方法就简单了，一劳永逸。

虽然网上又说关闭 `selinux` 会有安全问题。然而只是我虚拟机的 `linux` 开发机而已，并不是生产环境，没有太高的安全问题。

#### 方法一 修改安全策略

     chcon -t samba_share_t share

chcon 可以修改文件的安全上下文。重置windows建立的文件、文件夹的安全信息。也可以解决，但是比较麻烦，不方便。

#### 方法二 关闭 selinux

##### 永久关闭

修改 `/etc/selinux/config` 文件，设置

    SELINUX=disabled

然后重启linux。

##### 临时关闭

使用 `setenforce` 命令可以修改 `selinux` 模式。

- `setenforce 1` 设置 `selinux` 为 `enforcing` 模式；
- `setenforce 0` 设置 `selinux` 为 `permissive` 模式。

#### 其它方案

[https://wiki.centos.org/zh/HowTos/SetUpSamba](https://wiki.centos.org/zh/HowTos/SetUpSamba "https://wiki.centos.org/zh/HowTos/SetUpSamba") 有相当详细的解释和解决办法。有时间折腾的可以看看。

以上。