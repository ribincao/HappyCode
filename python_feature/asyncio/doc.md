
## 协程与任务

- 协程: async/await语法声明/执行一个协程函数
- 运行协程: 简单的调用一个协程并不会使其被调度执行, 要真正运行一个协程, asyncio提供了三种机制
    - asyncio.run()
    - await等待一个协程
    - asyncio.create_task()并发运行作为asyncio任务的多个协程
- 可等待对象: 可以在await语句中使用, 主要有三种类型
    - 协程, 可以通过`async def`定义一个协程函数, 可以在其他协程中被等待
    - 任务, 可通过`asyncio.create_task()`把一个协程函数封装成一个task
    - Future, 一种特殊的低层级可等待对象, 表示一个异步操作的最终结果. 当一个Future对象被等待意味着协程将保持等待知道该Future对象在其他地方操作完毕. 在asyncio中需要Future对象以便允许通过async/await使用基于回调的代码
- run(coro, *, debug=False): run()函数会运行传入的协程，负责管理asyncio事件循环，终结异步生成器，并关闭线程池. 当有其他 asyncio 事件循环在同一线程中运行时，此函数不能被调用.此函数总是会创建一个新的事件循环并在结束时关闭之。它应当被用作 asyncio 程序的主入口点，理想情况下应当只被调用一次
- create_task(coro, *, name=None): 将协程封装为一个Task并调度其执行, 返回 Task 对象
- sleep(delay, result=None, *, loop=None): 挂起当前任务，以允许其他任务运行, 将delay设为0将提供一个经优化的路径以允许其他任务运行
- asyncio.gather(*aws, loop=None, return_exceptions=False): 并发运行aws序列中的可等待对象
    - 如果 aws 中的某个可等待对象为协程，它将自动被作为一个任务调度
    - 如果所有可等待对象都成功完成，结果将是一个由所有返回值聚合而成的列表。结果值的顺序与 aws 中可等待对象的顺序一致
- asyncio.shield(aw, *, loop=None)¶: 保护一个可等待对象防止其被取消, 不同之处 在于如果包含它的协程被取消，在 something() 中运行的任务不会被取消。从 something() 的角度看来，取消操作并没有发生。然而其调用者已被取消，因此 "await" 表达式仍然会引发 CancelledError
    ```python
    try:
        ret = await shield(something())
    except CancelledError:
        ret = None
    ```
- asyncio.wait_for(aw, timeout, *, loop=None): 超时, 如果发生超时，任务将取消并引发 asyncio.TimeoutError.
    ```python
    try:
        await asyncio.wait_for(eternity(), timeout=1.0)
    except asyncio.TimeoutError:
        print('timeout!')
    ```
- asyncio.wait(aws, *, loop=None, timeout=None, return_when=ALL_COMPLETED): 简单等待, 并发地运行 aws 可迭代对象中的 可等待对象 并进入阻塞状态直到满足 return_when 所指定的条件, 返回两个 Task/Future 集合: (done, pending). 与 wait_for() 不同，wait() 在超时发生时不会取消可等待对象
    - FIRST_COMPLETED: 函数将在任意可等待对象结束或取消时返回。
    - FIRST_EXCEPTION: 函数将在任意可等待对象因引发异常而结束时返回。当没有引发任何异常时它就相当于 ALL_COMPLETED。
    - ALL_COMPLETED: 函数将在所有可等待对象结束或取消时返回。
- asyncio.to_thread(func, /, *args, **kwargs): 在不同的线程中异步地运行函数 func
    ```python
    asyncio.to_thread(blocking_io)
    ```
- asyncio.run_coroutine_threadsafe(coro, loop): 跨线程调度, 向指定事件循环提交一个协程(线程安全), 返回一个 concurrent.futures.Future 以等待来自其他 OS 线程的结果
    ```python
    # Create a coroutine
    coro = asyncio.sleep(1, result=3)
    # Submit the coroutine to a given loop
    future = asyncio.run_coroutine_threadsafe(coro, loop)
    # Wait for the result with an optional timeout argument
    assert future.result(timeout) == 3
    ```

## 流

- StreamReader
- StreamWriter

## 子进程

- create_subprocess_shell
- create_subprocess_exec

## 同步

- asyncio.Lock(*, loop=None): 实现一个用于 asyncio 任务的互斥锁。 非线程安全
    - acquire()
    - release()
    - locked()
    ```python
    lock = asyncio.Lock()

    # ... later
    async with lock:
        # access shared state
    ```
- asyncio.Event(*, loop=None): 事件对象, 该对象不是线程安全的. asyncio 事件可被用来通知多个 asyncio 任务已经有事件发生
    - set()
    - wait()
- asyncio.Condition(lock=None, *, loop=None): 条件对象, 该对象不是线程安全的. asyncio条件原语可被任务用于等待某个事件发生,然后获取对共享资源的独占访问
    - acquire()
    - release()
    - wait()
    - notify(n=1)
    - locked()
    ```python
    cond = asyncio.Condition()
    # ... later
    async with cond:
        await cond.wait()
    ```
- asyncio.Semaphore(value=1, *, loop=None): 信号量对象, 该对象不是线程安全的. 信号量会管理一个内部计数器, 该计数器会随每次 acquire() 调用递减并随每次 release() 调用递增
    ```python
    sem = asyncio.Semaphore(10)
    # ... later
    async with sem:
        # work with shared resource
    ```