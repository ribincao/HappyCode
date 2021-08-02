"""
author: ribincao
desc: Singleton Demo
"""
from typing import List
import threading
import time


#  装饰器
def singleton(cls):
    _instance = dict()

    def instance(*arg, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*arg, **kwargs)
        return _instance[cls]
    return instance


@singleton
class Test:

    def __init__(self):
        pass


class Singleton:

    # _lock = threading.Lock()

    def __init__(self, *args, **kwargs):
        # time.sleep(1)
        pass

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if not hasattr(Singleton, '_instance'):
            Singleton._instance = Singleton(*args, **kwargs)
        return Singleton._instance

    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(cls, '_instance'):
    #         with Singleton._lock:
    #             if not hasattr(cls, '_instance'):
    #                 Singleton._instance = super().__new__(cls)
    #
    #         return Singleton._instance


# def task(*args, **kwargs):
#     obj = Singleton()
#     print(f'obj： {obj}')


if __name__ == '__main__':
    t1, t2 = Test(), Test()
    print(f't1: {id(t1)}, t2: {id(t2)}')

    s1, s2 = Singleton(), Singleton()
    s3, s4 = Singleton.get_instance(), Singleton.get_instance()
    print(f's1: {id(s1)}, s2: {id(s2)}, s3: {id(s3)}, s4: {id(s4)}')

    # for i in range(10):
    #     t = threading.Thread(target=task, args=[i, ])
    #     t.start()
