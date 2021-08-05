import datetime
import threading
import time


def local_var():
    data = threading.local()
    data.pi = 3.14


class TestThread(threading.Thread):

    def __init__(self, para='hi'):
        super(TestThread, self).__init__()
        self.para = para

    def run(self):
        time.sleep(3)
        print(self.para)


def thread_class_demo():
    t = TestThread()
    t.start()


def test_thread(para='hi', sleep=3):
    time.sleep(sleep)
    print(para)


def thread_demo():
    t_hi = threading.Thread(target=test_thread)
    t_hello = threading.Thread(target=test_thread, args=('hello', 5))
    t_hi.start()
    t_hello.start()
    time.sleep(2)

    print("1")
    t_hi.join()
    print("t_hi finish")
    t_hello.join()
    print("Main t finish")

"""
Lock: 原始锁. Lock在锁定时不属于特定线程, 也就是说Lock可以在一个线程中上锁, 在另一个线程中解锁
Rlock: 重入锁. 只有当前线程才能释放本线程上的锁, acquire()/release() 对可以嵌套
"""
lock = threading.Lock()
global_resource = [None] * 5
def change_resource(para, sleep):
    lock.acquire()
    global global_resource
    for i in range(len(global_resource)):
        global_resource[i] = para
    print(f"global resource {global_resource}")
    lock.release()


def lock_demo():
    t_hi = threading.Thread(target=change_resource, args=('hi', 2))
    t_hello = threading.Thread(target=change_resource, args=('hello', 1))
    t_hi.start()
    t_hello.start()


condition = threading.Condition()
var = 0
def pre():
    print(f"var: {var}")
    return var
def thread_hi():
    condition.acquire()
    print("hi 1")
    condition.wait_for(pre)
    print("hi 2")
    condition.release()


def thread_hello():
    time.sleep(1)
    condition.acquire()
    global var
    var = 1
    print("change var")
    condition.notify()
    condition.release()
    print('ok')


def condition_demo():
    t_hi = threading.Thread(target=thread_hi)
    t_hello = threading.Thread(target=thread_hello)
    t_hi.start()
    t_hello.start()


sem = threading.Semaphore(3)
def thread_semaphore(index):
    sem.acquire() # sem -= 1
    time.sleep(2)
    print(f"thread_{index} is running ...")
    sem.release()


def semaphore_demo():
    for index in range(9):
        threading.Thread(target=thread_semaphore, args=(index, )).start()


event = threading.Event()
def student_exam(index):
    print(f"student_{index} wait paper...")
    event.wait()
    print(f"student_{index} start exam!")


def teacher():
    time.sleep(5)
    print("time get, start exam")
    event.set()


def event_demo():
    for index in range(5):
        threading.Thread(target=student_exam, args=(index, )).start()
    threading.Thread(target=teacher).start()


def print_time_sleep(n):
    while True:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        time.sleep(n)


def timer_demo():
    interval = 3
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    t = threading.Timer(interval, print_time_sleep, (interval, ))
    t.start()


def end():
    print("finished")
barrier = threading.Barrier(3, end)
def b_thread(sleep):
    time.sleep(sleep)
    print(f"barrier thread_{sleep} wait...")
    barrier.wait()
    print(f"barrier thread_{sleep} end")


def barrier_demo():
    for index in range(6):
        threading.Thread(target=b_thread, args=(index, )).start()


if __name__ == '__main__':
    barrier_demo()
