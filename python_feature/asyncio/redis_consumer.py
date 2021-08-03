import asyncio
from threading import Thread
import redis


def get_redis():
    conn_pool = redis.ConnectionPool(host='127.0.0.1')
    return redis.Redis(connection_pool=conn_pool)


def start_thread_loop(loop: asyncio.AbstractEventLoop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


async def worker(name):
    print('running ', name)
    await asyncio.sleep(2)
    return 'ret ' + name


def main():
    redis_conn = get_redis()
    
    loop = asyncio.new_event_loop()
    loop_thread = Thread(target=start_thread_loop, args=(loop, ))
    loop_thread.setDaemon(True)
    loop_thread.start()
    
    while True:
        msg = redis_conn.rpop('coro_test')
        print(msg)
        if msg:
            asyncio.run_coroutine_threadsafe(worker("ribin" + bytes.decode(msg, 'utf-8')), loop)
        else:
            break


if __name__ == '__main__':
    main()