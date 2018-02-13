title: "[erlang]supervisor(监控树)的使用和重启策略"
date: 2016-12-29 20:44:00
tags: [erlang]
---

## supervisor(监控树)的使用和重启策略

### 1. init函数

```erlang
init() ->
    {ok, {SupFlags, [ChildSpec,...]}} | ignore.
```

[ChildSpec,...] 是在init之后默认要启动的子进程。

### 2. SupFlags参数

{Type, Times, Sec}

- Type: 重启策略
    - one_for_one: 一个子进程终止，只重启该进程，在init的时候会启动参数内的子进程
    - simple_one_for_one: 同one_for_one，但是在init的时候不会启动子进程，需要动态调用启动
    - one_for_all: 一个子进程终止，将重启所有子进程
    - rest_for_one: 一个子进程终止，将按顺序重启这个子进程和之后顺序的子进程
- Times: 次数(监控频率)
- Sec: 秒数(监控频率)，如果在Sec秒内重启次数超过Times，则终止所有进程，并终止监控树，将由父进程决定它的命运

### 3. ChildSpec参数如下

```erlang
{Id, StartFunc, Restart, Shutdown, Type, Modules}

%% 或者

#{
    id => child_id(),
    start => mfaargs(),
    restart => restart(),
    shutdown => shutdown(),
    type => work(),
    modules => modules()
}
```

- Id 子进程ID标识符
- StartFunc = {M, F, A}: 子程序启动入口
- Restart: 重启方案
    - `permanent`: 如果app终止了，整个系统都会停止工作（application:stop/1除外）。
    - `transient`: 如果app以normal的原因终止，没有影响。任何其它终止原因都谁导致整个系统关闭。
    - `temporary`: app可以以任何原因终止。只产生报告，没有其它任何影响。
- Shutdown: 终止策略
    - `brutal_kill`: 无条件终止
    - 超时值(毫秒): 终止时，如果超时，则强制终止
    - `infinity`: 如果子进程是监控树，设置为无限大，等待其终止为止
- Type: 
    - `worker`: 普通子进程
    - `supervisor`: 子进程是监控树
- Modules: 
    - `dynamic`: 当子进程是gen_event
    - `[Module]`: 当子进程是监控树、gen_server或者gen_fsm，表示回调模块名称

### 4. 监控树操作

Sup通常可以为`?MODULE`

```erlang
% 启动监控树
supervisor:start_link(Sup, []).

% 启动一个子进程
supervisor:start_child(Sup, ChildSpec).

% 停止一个子进程
supervisor:terminate(Sup, Id).

% 删除一个子进程
supervisor:delete_child(Sup, Id).
```