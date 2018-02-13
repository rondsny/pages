title: "[docker]docker常用命令"
date: 2016-11-01 17:00:00
tags: [docker]
---

### 0. 学习的一些疑问

- 如何热更新镜像(images)？（你可以快速启动或者销毁容器。这种时间几乎是实时的）
- 如何热更新游戏服？
- 好处在于各个应用之间环境相互独立，即使某一个容器崩溃也不会影响到其它容器；
- 每个容器使用端口如何维护？（方法1写在Dockerfile里面，不灵活；方法2在run的时候-p指定）；
- 那这样的话，会存在好多linux用户，相当于每一个容器就要维护一个物理机（虚拟）；
- 需要一套工具来管理维护镜像、容器的操作和状态；
- 目前主流使用docker都是应用到哪些场景中？

### 1. docker的二个软件

- Docker: 开源的容器虚拟化平台；
- Docker Hub: Software-as-a-Service平台，用来共享和管理docker容器。

### 2. docker的三大模块

- Docker images.(镜像)
- Docker registries.(仓库)
- Docker container.(容器)

### 3. 常用命令

#### 3.1. 常用镜像命令

- docker image(查看镜像信息)
- docker build(创建镜像)
    - Dockerfile
        - '#注释'
        - FROM 基于哪个镜像为基础
        - MAINTAINER 维护者信息
        - RUN 运行指令
        - ADD 复制本地文件到镜像
        - EXPOSE 设置开放端口
        - CMD 容器启动后允许的程序
        - WORKDIR 切换工作目录
    - -t 添加tag
    - build后面需要接路径

#### 3.2. 少用镜像命令

- docker pull(获取镜像)
- docker push(上传镜像)
- docker search(搜索镜像)
    - -s N 只搜索指定星级以上的镜像
- docker rmi(删除镜像)
- docker tag [id] [new name:tag] (修改tag)
- docker save(保存镜像)
- docker load(加载镜像)
    - docker load --input xxx.tar
    - docker load < xxx.tar
    - load与import的区别，镜像是完整的与快照是丢弃历史记录和元数据信息的
- docker rmi $(docker images -q -f "dangling=true")(清理所有未打过标签的本地镜像)

#### 3.3. 常用容器命令

- docker run([下载镜像并]启动容器)
    - -t 分配一个伪终端
    - -i 打开标准输入
    - -d 后台运行
    - -v <path> 创建并挂载数据卷(可有多个)
    - --volumes-from 挂载数据卷(可有多个)
    - -p 指定映射端口 (ip:Port:containerPort/udp|ip::containerPort|port:containerPort)
    - -P 随机映射端口
    - --name 自定义容器名字
    - --rm 终止后立即删除容器
    - --link <name>:<alias> 容器互联
- docker start(启动已终止容器)
- docker stop(终止容器)
- nsenter(进入容器)(推荐)

```bash
PID=$(docker inspect --format "{{ .State.Pid }}" <container ID>)
nsenter --target $PID --mount --uts --ipc --net --pid
```

#### 3.4. 少用容器命令

- docker commit(提交容器)
    - -m --massage="" 提交信息
    - -a --author="" 作者信息
    - -p --pause=true 提交时暂停容器运行
- docker attach(进入容器)
- docker ps(查看正在运行的容器)
    - -a 查看已终止
- docker logs [container ID or NAMES] 查看(后台)运行日志
- docker export(导出容器为文件)
    - docker export <container ID> > xxx.tar
- docker import(文件快照导入镜像)
    - cat xxx.tar | docker import - test/name:v1.0
    - docker import http://xxx.tgz test/name
- docker rm(删除容器)
    - 默认不会删除运行中的容器
    - docker rm $(docker ps -a -q) 清理所有处于终止状态的容器
    - -v 同时删除数据卷

### 4. 安装

### 4.1. 在CentOS7中安装

    curl -sSL https://get.docker.com/ | sh        //下载官服脚本按照
    chkconfig docker on                           //设置开机自动启动

### 4.2. 在CentOS6中安装

#### 4.2.1. 添加yum软件源

    tee /etc/yum.repo.d/docker.repo << 'EOF'
    [dockerrepo]
    name=Docker Repository
    baseurl=https://yum.dockerproject.org/repo/main/centos/$releasever/
    enabled=1
    gpgcheck=1
    gpgkey=https://yum.dockerproject.org/gpg
    EOF

#### 4.2.2. 安装docker

    yum update
    yum install -y docker-engine

#### 4.2.3. No module named yum 

如果在执行`yum update`的时候出现了`No module named yum`错误，可能是存在与yum不对应的python版本引起。可以通过修改yum和yum-updatest的执行脚本（`/usr/bin/yum`和`/usr/bin/yum-updatest`）的注释来指定python版本。譬如：

    #!/usr/bin/python
    修改为
    #!/usr/bin/python2.6


### 5. 基础环境

可以下载bashrc_docker文件，加载到环境.bashrc中，其可以提供一些方便的命令用于做一些比较复杂的过程。

`.bashrc_docker`(https://raw.githubusercontent.com/yeasy/docker_practice/master/_local/.bashrc_docker) 定义了以下命令
    - docker-pid(获取容器pid)
    - docker-enter(进入容器)

下载和加载到linux环境中：

    wget -P ~ https://raw.githubusercontent.com/yeasy/docker_practice/master/_local/.bashrc_docker
    echo "[ -f ~/.bashrc_docker ] && . ~/.bashrc_docker" >> ~/.bashrc;source ~/.bashrc

### 6. 仓库

#### 6.1. 私有仓库

官服提供了一个docker-registry镜像来供私有仓库的搭建。

    docker run -d -p 80:5000 registry

    vi /etc/docker/daemon.json
    {"insecure-registries":["myregistry.example.com:5000"]}

    cul http://x.x.x.x:2010/v2/linerl/tags/list

API文档：https://github.com/docker/distribution/blob/master/docs/spec/api.md

### 7. 学习后的一些结论

- 本身是虚拟机技术实现的服务器大多数带有随时可扩展升级的性质，没有资源分配的需求，没有必要用到docker；
- docker适合在做负载均衡的短链接的web服务上面，应用场景都是以镜像、容器为操作单位的最佳；
- 如果有业务可以做到镜像、容器来维护就可以的，说明这个业务就很合适使用docker。