title: "[python]自动化将markdown文件转成html文件"
date: 2016-09-22 18:00:00
tags: [python,markdown,ci]
---

### 一、背景

我们项目开发人员写的文档都是`markdown`文件。对于其它组的同学要进行阅读不是很方便。每次编辑完`markdown`文件，我都是用软件将`md`文件转成`html`文件。刚开始转的时候，还没啥，转得次数多了，就觉得不能继续这样下去了。作为一名开发人员，还是让机器去做这些琐碎的事情吧。故写了两个脚本将`md`文件转成`html`文件，并将其放置在web服务器下，方便其他人员阅读。

主要有两个脚本和一个定时任务：

- 一个python脚本，主要将`md`文件转成`html`文件；
- 一个shell脚本，主要用于管理逻辑；
- 一个linux定时任务，主要是定时执行shell脚本。

### 二、用python将markdown转成html

#### 2.1 python依赖库

使用python的markdown库来转换md文件到html依赖两个库：

- pip install markdown
- pip install importlib

#### 2.2 核心代码

核心代码其实只有一句，执行 `markdown.markdown(text)`就可以获得生成的html的原文。

```python
    input_file = codecs.open(in_file, mode="r", encoding="utf-8")
    text = input_file.read()
    html = markdown.markdown(text)
```

#### 2.3 html编码和html样式

直接`markdown.markdown(text)`生成的html文本，非常粗略，只是单纯的html内容。而且在浏览器内查看的时候中文乱码(在chrome中)，没有好看的css样式，太丑了。

![乱码无样式](/pics/451_luanma.png)

解决办法也很简单，在保存文件的时候，将`<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />`和css样式添加上。就这么简单解决了。

![带css样式](/pics/451_piaoliang.png)

#### 2.4 完整python内容

- 读取md文件；
- 将md文件转成html文本；
- 添加css样式和保存html文本。

python代码内容：

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 使用方法 python markdown_convert.py filename

import sys
import markdown
import codecs


css = '''
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<style type="text/css">
<!-- 此处省略掉markdown的css样式，因为太长了 -->
</style>
'''

def main(argv):
    name = argv[0]
    in_file = '%s.md' % (name)
    out_file = '%s.html' % (name)

    input_file = codecs.open(in_file, mode="r", encoding="utf-8")
    text = input_file.read()
    html = markdown.markdown(text)

    output_file = codecs.open(out_file, "w",encoding="utf-8",errors="xmlcharrefreplace")
    output_file.write(css+html)

if __name__ == "__main__":
   main(sys.argv[1:])

```

### 三、shell逻辑

#### 3.1 逻辑说明

建立一个shell文件，用于进行逻辑处理，主要操作如下：

- 更新svn文件，将最新的md文件更新下来(此处假设md文件是`测试文档.md`)；
- 执行`python markdown_convert.py $NAME`将md文件转成html文件(生成`测试文档.html`)；
- 将转好的html迁移到web路径下(移动到`html/测试文档.html`)；
- 启动一个web服务(此处用的是python的`SimpleHTTPServer`的web服务器).

#### 3.2 完整shell逻辑

```bash
#!/bin/bash

NAME='测试文档'

## 更新代码
svn update

## 删除html文件
if [ -f "$NAME.html" ];then
    rm "$NAME.html"
fi

## 生成html
if [ -f "$NAME.md" ];then
    python markdown_convert.py $NAME
fi

## 生成html目录
if [ ! -d "html" ];then
    mkdir "html"
fi

## 拷贝html文件
if [ -f "$NAME.html" ];then
    mv -f "$NAME.html" "html/"
fi

## 开启web服务器
PID=`ps aux | grep 'python -m SimpleHTTPServer 8080' | grep -v 'grep' | awk '{print $2}'`

if [ "$PID" = "" ];then
    cd html
    nohup python -m SimpleHTTPServer 8080 &
    echo 'start web server'
else
    echo 'already start'
fi

```

### 四、linux定时任务

在shell命令下输入`crontab -e`进入`linux`定时任务编辑界面。在里面设置`markdown2web.sh`脚本的定时任务：

```bash
## 更新文档
*/10 * * * * cd /home/xxx/doc; sh markdown2web.sh > /dev/null 2>&1
```

设置每10分钟执行一次`markdown2web.sh`脚本，当然也可以根据需求修改频率。