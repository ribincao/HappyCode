import asyncio
import random
import time


async def worker(name, queue):
    while True:
        #  每个 get() 用于获取一个任务，任务最后调用 task_done() 告诉队列，这个任务已经完成
        sleep_for = await queue.get()
        await asyncio.sleep(sleep_for)
        queue.task_done()
        print(f"{name} has slept for {sleep_for:.2f} seconds.")


async def run():
    queue = asyncio.Queue()

    total_sleep_time = 0
    for _ in range(20):
        sleep_for = random.uniform(0.05, 1.0)
        total_sleep_time += sleep_for
        #  不阻塞的放一个元素入队列
        queue.put_nowait(sleep_for)

    tasks = []
    for i in range(3):
        task = asyncio.create_task(worker(f'worker-{i}', queue))
        tasks.append(task)

    started_at = time.monotonic()
    #  阻塞至队列中所有的元素都被接收和处理完毕
    await queue.join()
    total_sleep_for = time.monotonic() - started_at

    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)
    print("===")
    print(f"3 workers slept in parallel for {total_sleep_for:.2f} seconds.")
    print(f"total expected sleep time: {total_sleep_time:.2f} seconds.")


if __name__ == '__main__':
    asyncio.run(run())
