import time

from gevent import monkey as monkey
import gevent

#  猴子补丁修改自带标准库
monkey.patch_socket()


def hello(n):
    for i in range(1, n + 1):
        print(gevent.getcurrent(), i)
        #  故意设置sleep交出控制权, 模拟I/O等待
        gevent.sleep(0)


#  只有一个线程
def run():
    #  创建 3 个 greenlet 协程
    g1 = gevent.spawn(hello, 5)
    g2 = gevent.spawn(hello, 5)
    g3 = gevent.spawn(hello, 5)

    g1.join()
    g2.join()
    g3.join()


def run2():
    gevent.joinall([
        gevent.spawn(hello, 3),
        gevent.spawn(hello, 4),
        gevent.spawn(hello, 5),
    ])


if __name__ == '__main__':
    # run()
    run2()
