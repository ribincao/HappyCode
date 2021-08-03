import multiprocessing
import os
from multiprocessing import Pool, Process, Pipe, Lock, Value, Array


def info(name):
    print(name)
    print(f"module name: {__name__}")
    print(f"parent pid: {os.getppid()}")
    print(f"pid: {os.getpid()}")


def f(x):
    info("function f")
    print(f"return: {x * x}")


def pool_demo():
    with Pool(5) as p:
        p.map(f, [1, 2, 3])


def process_demo():
    p = Process(target=f, args=(10, ))
    p.start()
    p.join()


def g(q):
    q.put('hello')


def start_method():
    """
    1. spawn
    2. fork
    3. forkserver
    """
    multiprocessing.set_start_method('spawn')
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=g, args=(q, ))
    p.start()
    print(q.get())
    p.join()


def context_demo():
    ctx = multiprocessing.get_context()
    q = ctx.Queue()
    p = ctx.Process(target=g, args=(q, ))
    p.start()
    print(q.get())
    p.join()


def h(conn):
    info("h")
    conn.send([42, None, 'hello'])
    conn.close()


def pipe_demo():
    parent_conn, child_conn = Pipe()
    p = Process(target=h, args=(child_conn, ))
    p.start()
    print(parent_conn.recv())
    p.join()


def s(lock, index):
    # info("s")
    lock.acquire()
    try:
        print(f"hello {index}")
    finally:
        lock.release()


def process_sync_demo():
    """ 锁来进行同步 """
    lock = Lock()
    for idx in range(8):
        Process(target=s, args=(lock, idx)).start()


def y(num, arr):
    num.value = 3.1415926
    for i in range(len(arr)):
        arr[i] = -arr[i]


def share_demo():
    """ 共享内存 """
    num = Value('d', 0.0)
    arr = Array('i', range(10))

    p = Process(target=y, args=(num, arr))
    p.start()
    p.join()

    print(num.value)
    print(arr[:])


if __name__ == '__main__':
    share_demo()
