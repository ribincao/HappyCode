import time
from datetime import datetime
from threading import Timer


def print_time_sleep(n):
    while True:
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        time.sleep(n)  # 阻塞


def print_time_timer(inc):
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    t = Timer(inc, print_time_timer, (inc, ))  # 非阻塞
    t.start()


if __name__ == '__main__':
    print_time_sleep(2)
    print_time_timer(1)
