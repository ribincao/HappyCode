class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance


def singleton(cls):
    _instance = dict()

    def instance(*arg, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*arg, **kwargs)
        return _instance[cls]
    return instance


class S(Singleton):

    def __init__(self, name):
        super(S, self).__init__()
        self.name = name


@singleton
class Test:
    pass


def task():
    obj = Test()
    print(id(obj))


if __name__ == '__main__':
    from threading import Thread
    for i in range(5):
        Thread(target=task).start()