"""
    - 所有的 Python 的用户定义类，都是 type 这个类的实例
    - 用户自定义类，只不过是 type 类的 __call__ 运算符重载
    - metaclass 是 type 的子类，通过替换 type 的 __call__ 运算符重载机制，“超越变形”正常的类
"""


class MyMeta(type):
    def __init__(self, name, bases, dic):
        super().__init__(name, bases, dic)
        print('MyMeta.__init__')

    def __new__(cls, *args, **kwargs):
        print('MyMeta.__new__')
        # print(cls.__name__)
        return type.__new__(cls, *args, **kwargs)

    def __call__(cls, *args, **kwargs):
        print('MyMeta.__call__')
        obj = cls.__new__(cls)
        cls.__init__(cls, *args, **kwargs)
        return obj


class Demo(metaclass=MyMeta):

    def __init__(self, name):
        print('Demo.__init__')
        self.name = name

    def __new__(cls, *args, **kwargs):
        print('Demo.__new__')
        return object.__new__(cls)


class Test:

    data = ""

    def __init__(self, name):
        self.name = name


if __name__ == '__main__':
    t1 = type('Test', (), {'data': 1, 'name': 'ribincao'})
    t2 = Test("ribincao")
    t2.data = 3
    print(t1, type(t1), t1.data, t1.name)
    print(t2, type(t2), t2.data, t2.name)
    t = t1()
    print(t, type(t), t.data, t.name)

    # MyMeta.__new__
    # MyMeta.__init__
    # MyMeta.__call__
    # Demo.__new__
    # Demo.__init__
    d = Demo('ribincao')
