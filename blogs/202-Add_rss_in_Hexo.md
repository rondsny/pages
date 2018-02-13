title: "[hexo]在hexo内添加RSS和sitemap"
date: 2015-03-12 15:28:01
tags: hexo
---

### 一、添加RSS
博客来说，RSS的重要性可想而知。

#### 1. 安装hexo rss插件
hexo提供了生成RSS xml的插件`hexo-generator-feed`，执行`npm install hexo-generator-feed`即可。

#### 2. 配置
编辑`blog/_config.yml`文件。在里面添加查看配置，如下

    plugins: 
      hexo-generator-feed

还要修改主题的配置文件`blog/theme/_config.yml`。在rss里面配置`rss: /atom.xml`。在菜单里面添加RSS菜单。

    menu: 
      Home: / 
      Archives: /archives 
      Rss: /atom.xml

### 二、添加sitemap
当关注seo的时候，sitemap也同样重要。

#### 1. 安装hexo sitemap插件
同样，执行命令`npm install hexo-generator-sitemap`即可完成插件的安装。

#### 2. 配置
一样修改`blog/_config.yml`文件，添加上插件名称

    plugins: 
      hexo-generator-feed
      hexo-generator-sitemap 
      
### 三、其它
其实两个插件是在`hexo g`的时候生成atom.xml 文件和sitemap.xml 文件。由于sitemap.xml 是对搜索引擎服务的，所以不需要显示在博客里面。而Rss是要给读者收藏的，需要在菜单里面添加显示。当然你不喜欢在菜单里面显示可以直接修改模板显示在你喜欢的地方。如编辑`blog/theme/[light]/layout/_partial/header.ejs`文件：

    <ul>
    <% for (var i in theme.menu){ %>
      <li><a href="<%- theme.menu[i] %>"><%= i %></a></li>
    <% } %>
    <li><a href="/atom.xml">RSS</a></li>
    </ul>
    
可以不配置menu达到相同的效果。