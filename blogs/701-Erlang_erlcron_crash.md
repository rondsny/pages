title: "[erlang]一次erlcron崩溃引起的事故分析"
date: 2016-03-24 13:34:57
tags: erlang
---

### 事故背景

由于误操作在`erlcron`设置了一个超过3个月后的定时任务。然后第二天之后发现每天的daily reset没有被执行，一些定时任务也没有被执行。瞬间感觉整个人都不好了，怎么无端端就不执行了呢。

通过排查日志，发现了以下报错：

    2016-03-22 16:54:32.014 [error] gen_server ecrn_control terminated with reason: no case clause matching {ok,[<0.14123.1577>,<0.13079.1576>,<0.25254.1569>,<0.13402.1577>,...]} in ecrn_control:internal_cancel/1 line 111
    2016-03-22 16:54:32.015 [error] CRASH REPORT Process ecrn_control with 0 neighbours exited with reason: no case clause matching {ok,[<0.14123.1577>,<0.13079.1576>,<0.25254.1569>,<0.13402.1577>,...]} in ecrn_control:internal_cancel/1 line 111 in gen_server:terminate/6 line 744
    
我擦，`ecrn_control`都崩了，怎么回事。

找到具体出错的代码：

    internal_cancel(AlarmRef) ->
        case ecrn_reg:get(AlarmRef) of
            undefined ->
                undefined;
            {ok, [Pid]} ->
                ecrn_agent:cancel(Pid)
        end.

发现调用`ecrn_reg:get(AlarmRef)`被返回了{ok, List}，而且这个List的数据远不止一个。明显在设置那个超过3个月的定时任务的时候，`ecrn_reg`被注册进了脏数据。

### 事故重现

#### 先设置几个正常的定时任务

    > erlcron:cron({{once, 1000}, {io, fwrite, ["Hello, world!~n"]}}).
    > erlcron:cron({{once, 1000}, {io, fwrite, ["Hello, world!~n"]}}).
    > erlcron:cron({{once, 1000}, {io, fwrite, ["Hello, world!~n"]}}).

查看`observer:start()` 可以看到进程树如下：

![](http://i.imgur.com/H4oSaR0.png)

#### 再设置一个4294968秒之后的定时任务

    > erlcron:cron({{once, 4294968}, {io, fwrite, ["Hello, world!~n"]}}).

结果就gg了，好多崩溃信息是不是：

    22:49:16.818 [error] CRASH REPORT Process <0.5822.64> with 0 neighbours crashed with reason: timeout_value in gen_server:loop/6 line 358
    22:49:16.818 [error] Supervisor ecrn_cron_sup had child ecrn_agent started with ecrn_agent:start_link(#Ref<0.0.11.11209>, {{once,4294968},{io,fwrite,["Hello, world!~n"]}}) at <0.5822.64> exit with reason timeout_value in context child_terminated
    22:49:16.819 [error] CRASH REPORT Process <0.5701.64> with 0 neighbours crashed with reason: timeout_value in gen_server:loop/6 line 358
    22:49:16.821 [error] Supervisor ecrn_cron_sup had child ecrn_agent started with ecrn_agent:start_link(#Ref<0.0.11.11209>, {{once,4294968},{io,fwrite,["Hello, world!~n"]}}) at <0.5701.64> exit with reason timeout_value in context child_terminated
    22:49:16.821 [error] CRASH REPORT Process <0.6237.64> with 0 neighbours crashed with reason: timeout_value in gen_server:loop/6 line 358
    22:49:16.821 [error] Supervisor ecrn_cron_sup had child ecrn_agent started with ecrn_agent:start_link(#Ref<0.0.11.11209>, {{once,4294968},{io,fwrite,["Hello, world!~n"]}}) at <0.6237.64> exit with reason timeout_value in context child_terminated
    22:49:16.821 [error] CRASH REPORT Process <0.5862.64> with 0 neighbours crashed with reason: timeout_value in gen_server:loop/6 line 358
    22:49:16.821 [error] Supervisor ecrn_cron_sup had child ecrn_agent started with ecrn_agent:start_link(#Ref<0.0.11.11209>, {{once,4294968},{io,fwrite,["Hello, world!~n"]}}) at <0.5862.64> exit with reason timeout_value in context child_terminated

    ...(总共有25条)

再看一下进程数：

![](http://i.imgur.com/TSYo5CH.png)

我擦，为毛原来的 scrn_agent 进程也没有了。

可以发现，erlcron 在尝试了25次设置 这个定时任务之后，也就是 scrn_agent 崩溃了25次之后，原来设置的三个正常的定时任务的scrn_agent 进程也没有掉了。
也就是说，不但我新设置的定时任务没有成功，而且我原来正常的定时任务也没有掉了。

再看一下崩溃日志里面的崩掉的进程号，每一个都是不一样的。可以推算其实原来的报错`ecrn_reg:get(AlarmRef)`获取到了多个Pid，其实就是这里插入失败的定时任务产生的25个Pid。也就是说，虽然`ecrn_agent`进程崩溃了，但是`ecrn_reg`还是保存了这些Pid。所以在取消这些定时任务的时候，`ecrn_reg:get(AlarmRef)`返回的内容在`internal_cancel(AlarmRef)`没有被匹配到。

### 为什么是4294968，其实是2^32

为什么设置了`4294968`秒后的定时任务就崩溃了。这个数估计很多人很熟悉，`2^32=4294967296`，而`4294968000`也就是刚好大于`2^32`。即，如果设置的定时任务超过了`2^32`毫秒，在`erlcron`里面就不支持了。


查看`gen_server:loop`的源码，找到引起崩溃的代码：

![](http://i.imgur.com/w9NJViE.png)

    loop(Parent, Name, State, Mod, hibernate, Debug) ->
        proc_lib:hibernate(?MODULE,wake_hib,[Parent, Name, State, Mod, Debug]);
    loop(Parent, Name, State, Mod, Time, Debug) ->
        Msg = receive
    	      Input ->
    		    Input
    	  after Time ->
    		  timeout
    	  end,
        decode_msg(Msg, Parent, Name, State, Mod, Time, Debug, false).

可以发现引起崩溃的，358行是一段`receive`代码。也就是说`receive`是不支持超过`2^32`大小的。

自测了一下，的确如果`receive`的`after`后面如果是大于等于`2^32`的数值就会出现`bad receive timeout value`的报错。查看官方解释，已经明确说明不能大于`32位`大小。

> ExprT is to evaluate to an integer. The highest allowed value is 16#FFFFFFFF, that is, the value must fit in 32 bits. receive..after works exactly as receive, except that if no matching message has arrived within ExprT milliseconds, then BodyT is evaluated instead. The return value of BodyT then becomes the return value of the receive..after expression.

*引用自：http://erlang.org/doc/reference_manual/expressions.html*

再回到`erlcron`， 在 `ecrn_agent:start_link`的时候，`ecrn_agent:init`执行完`ecrn_reg:register(JobRef, self())`返回`{ok, NewState, Millis}`到`gen_server`之后，Millis如果超过`2^32`在`gen_server:loop`就会引起`gen_server`的`timeout_value`异常退出。

    %% @private
    init([JobRef, Job]) ->
        State = #state{job=Job,
                       alarm_ref=JobRef},
        {DateTime, Actual} = ecrn_control:datetime(),
        NewState = set_internal_time(State, DateTime, Actual),
        case until_next_milliseconds(NewState, Job) of
            {ok, Millis} when is_integer(Millis) ->
                ecrn_reg:register(JobRef, self()),
                {ok, NewState, Millis};
            {error, _}  ->
                {stop, normal}
        end.

### 最后

这坑踩的，有点郁闷。其实这跟`erlcron`也没关系，也不是`gen_server`的问题。而是`erlang`自身`receive`不支持2^32引起的。继续往下查其实可以发现，再往下是其它语言写的了。

    -module(prim_eval).
    
    %% This module is simply a stub which abstract code gets included in the result
    %% of compilation of prim_eval.S, to keep Dialyzer happy.
    
    -export(['receive'/2]).
    
    -spec 'receive'(fun((term()) -> nomatch | T), timeout()) -> T.
    'receive'(_, _) ->
        erlang:nif_error(stub).

*与君共勉*