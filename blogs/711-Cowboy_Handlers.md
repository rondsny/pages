title: "[翻译][erlang]cowboy handler模块的使用"
date: 2016-11-23 20:00:00
tags: [erlang, cowboy]
---

### 关于Cowboy

Cowboy是基于Erlang实现的一个轻量级、快速、模块化的http web服务器。

### Handlers

用于处理HTTP请求的程序处理模块。

### Plain HTTP Handlers（常规Handlers）

Cowboy里面的handler最基础的事情就是实现 `init/2` 回调函数，处理请求，发送客户端响应（可选），最后返回。
Cowboy根据 `router configuration` （路由配置）接收请求并初始化State。
下面是一个不做任何处理的handler：

    init(Req, State) ->
        {ok, Req, State}

Cowboy为了保证每一个相应都能有客户端响应，尽管上面例子没有发送客户端返回，客户端仍然会收到一个 `204 No Content` 的响应。

下面是一个有返回响应的例子：

    init(Req0, State) ->
        Req = cowboy_req:reply(200, [
            {<<"content-type">>, <<"text/plain">>}
        ], <<"Hello, World!">>, Req0),
        {ok, Req, State}.

当调用了 `cowboy:req/4`, Cowboy会马上返回一个客户端响应。

最后我们返回一个三元组。`ok` 表示handler允许成功，然后返回处理过后的 `Req` 给Cowboy。
三元组的最后一个元素是一个贯穿在handler所有回调一个state。常规的HTTP handlers一般只附加一个回调函数，`terminate/2`是一个很少使用的可选的回调函数。


### Other Handlers（其它Handlers）

`init/2` 回调函数也可以用来告诉cowboy，这是一个不同类型的handler，Cowboy应该做一些其他处理。为了方便使用，如果返回handler类型的模块名称，就可以切换handler处理模块。

Cowboy提供了三种可选handler类型：cowboy_reset, Cowboy_websocke和cowboy_loop。另外也可以自己定义handler类型。

切换非常简单，用handler类型替换掉返回的 `ok` 就可以了。下面是一个切换为 Websocket handler 的代码片段。

    init(Req, State) ->
        {cowboy_websocket, Req, State}.

也可以切换到一个自定义的handler模块：

    init(Req, State) ->
        {my_handler_type, Req, State}.

如何使用自定义的handler类型可以查看`Sub protocols` 章节（https://ninenines.eu/docs/en/cowboy/2.0/guide/sub_protocols）。

### Cleaning up

除了Websocket handlers，其它所有类型都提供可选回调函数`terminate/3`：

    terminate(_Reason, _Req, _State) ->
        ok.

这个回调函数是为了cleanup保留下来的。该函数不能发送响应给客户端。也没有其他返回值（只能返回`ok`）。

`terminate/3`之所以是可选是因为其极少会用到。Cleanup应该在各自的进程中直接处理。（通过监控handler进程来知道其何时退出）

Cowboy不会在不同的请求重复使用进程（应该是http短链接设计引起的）。进程在返回之后很快就会被销毁。


### Others

英文官方原文：

https://ninenines.eu/docs/en/cowboy/2.0/guide/handlers/#_plain_http_handlers