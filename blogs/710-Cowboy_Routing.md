title: "[翻译][erlang]cowboy路由模块使用"
date: 2016-11-23 14:00:00
tags: [erlang, cowboy]
---

### 关于Cowboy

Cowboy是基于Erlang实现的一个轻量级、快速、模块化的http web服务器。

### Routing（路由）

本文官方原文：http://ninenines.eu/docs/en/cowboy/1.0/guide/routing/

默认情况下，Cowboy不会做什么事情。
为了使Cowboy可用，需要映射URL和处理请求的Erlang模型（Module），这个过程，我们称之为路由（routing）。
当Cowboy接收到一个请求，通过路由，Cowboy就会尝试去匹配到相应请求的主机和资源路径。如果匹配成功，那么相关的Erlang代码就会被执行。
每个主机会给出相应的路由规则。Cowboy首先会匹配主机，然后尝试寻找匹配的路径。
在使用Cowboy之前需要先编译路由。

### Structure（结构）

路由一般定义成以下结构

    Routes = [Host1, Host2, ... HostN].

每个主机包含匹配规则（HostMatch）、限制规则（非必须）（Constraints）和一个由路径组成的路由列表（PathsList）。

    Host1 = {HostMatch, PathsList}.
    Host2 = {HostMatch, Constraints, PathsList}.

由路径组成的路由列表与主机列表类似。

    PathsList = [Path1, Path2, ... PathN].

而路径（path）包含匹配路径规则、限制规则（非必须）、处理逻辑的module和会被初始化的选项参数。

    Path1 = {PathMatch, Handler, Opts}.
    Path2 = {PathMatch, Constraints, Handler, Opts}.

下面内容为匹配语法和限制选项。

### Match syntax（匹配语法）

匹配语法用来关联主机名字和相应的handler路径。
主机的匹配语法和路径的匹配语法类似，只有轻微的区别。譬如，他们分隔符是不一样的。而且主机是从最后开始匹配的，而路径是不是。
（其实说了老半天，这不就是一个普通的URL嘛。URL的前半部分为主机IP或域名，这里称之为HOST，即主机。而后半部分为路径）
除了特殊情况，最简单的匹配就是只有主机或者只有路径的匹配。他的值可以为string() 或binary() 类型。
    
    PathMatch1 = "/".
    PathMatch2 = "/path/to/resource".
     
    HostMatch1 = "cowboy.example.org".

正如你所见，所有的路径都是由斜杠开始的。注意，下面两条路径对于路由而言是一样的。

    PathMatch2 = "/path/to/resource".
    PathMatch3 = "/path/to/resource/".

而对于主机名，最后有点和没有点对于路由来说也是一样的。同样，在前面多一个点和少一个点也是一样的。

    HostMatch1 = "cowboy.example.org".
    HostMatch2 = "cowboy.example.org.".
    HostMatch3 = ".cowboy.example.org".

因此能够提取主机和路径的数据段并且存储在Req 对象供后面使用。我们称之为值绑定。
绑定语法非常简单。由冒号字符（:）开头，一直到数据段的结尾的这个数据段是我们的绑定名称，会被保存。

    PathMatch = "/hats/:name/prices".
    HostMatch = ":subdomain.example.org".

如果这两个最终匹配，那么就会有两个绑定定义，分布是:subdomain 和:name ，每个包含被定义的数据段。例如，这个URL地址 http://test.example.org/hats/wild_cowboy_legendary/prices 会将 test绑定到subdomain ,并将wild_cowboy_legendary 绑定到 name 。他们通过cowboy_req:binding/{2,3} 函数检索出来的。绑定名字必须是原子（atom）类型。

还有一种特殊的绑定名字，它模仿erlang的下划线变量。任意内容都能与下划线（_）相匹配，但是数据会被丢弃。最有用的场景就是去匹配多个域名。

    HostMatch = "ninenines.:_".

类似地，也可以添加可选内容。中括号内的内容都是可选的。

    PathMatch = "/hats/[page/:number]".
    HostMatch = "[www.]ninenines.eu".

并且可选内容可以内嵌

    PathMatch = "/hats/[page/[:number]]".

还可以使用[...] 来获取主机名或路径剩余的部分。匹配主机的时候，需要放在最前面；匹配路径的时候是放在最后面。分别使用cowboy_req:host_info/1 和 cowboy_req:path_info/1 函数可以找到他们。

    PathMatch = "/hats/[...]".
    HostMatch = "[...]ninenines.eu".

如果一个绑定变量出现了两次，那么只有这两个位置的值相同的时候才会匹配成功。

    PathMatch = "/hats/:name/:name".

在可选变量里面也是一样的，在下面这个例子中，如果可选变量有值，必须两个绑定变量的值都一样才可匹配到。

    PathMatch = "/hats/:name/[:name]".

如果一个绑定变量出现在主机名和路径当中，他们需要是相同的才能匹配。

    PathMatch = "/:user/[...]".
    HostMatch = ":user.github.com".

当然也有两种特殊情况，第一种使用下划线变量（_）可以匹配任意的主机名和路径。

    PathMatch = '_'.
    HostMatch = '_'.

第二种，使用通配符星号（*）来匹配。

    HostMatch = "*".

### Constraints（约束）

关于这段没看懂，下面是英文原文：

> After the matching has completed, the resulting bindings can be tested against a set of constraints. Constraints are only tested when the binding is defined. They run in the order you defined them. The match will succeed only if they all succeed.

> They are always given as a two or three elements tuple, where the first element is the name of the binding, the second element is the constraint's name, and the optional third element is the constraint's arguments.

> The following constraints are currently defined:

> - {Name, int}
> - {Name, function, fun ((Value) -> true | {true, NewValue} | false)}
> 
The int constraint will check if the binding is a binary string representing an integer, and if it is, will convert the value to integer.

> The function constraint will pass the binding value to a user specified function that receives the binary value as its only argument and must return whether it fulfills the constraint, optionally modifying the value. The value thus returned can be of any type.

> Note that constraint functions SHOULD be pure and MUST NOT crash.

### Compilation（编译/收集）

在传递给Cowboy之前，定义的结构首先要先编译。才能是Cowboy有效查找到正确的handler，并执行，而不必重复地解析路由。
编译通过调用cow_router:compile/1 函数进行。
    
    Dispatch = cowboy_router:compile([
        %% {HostMatch, list({PathMatch, Handler, Opts})}
        {'_', [{'_', my_handler, []}]}
    ]),
    %% Name, NbAcceptors, TransOpts, ProtoOpts
    cowboy:start_http(my_http_listener, 100,
        [{port, 8080}],
        [{env, [{dispatch, Dispatch}]}]
    ).

注意，如果结构不正确，函数会返回{error, badarg}。

### Live update（热更新）

使用cowboy:set_env/3 函数可以更新当前的路由列表。这会应用到所有的监听器中。

    cowboy:set_env(my_http_listener, dispatch,
        cowboy_router:compile(Dispatch)).
    
注意，设置之前还是需要编译的哦。