"""
	- 所有的 Python 的用户定义类，都是 type 这个类的实例
	- 用户自定义类，只不过是 type 类的 __call__ 运算符重载
	- metaclass 是 type 的子类，通过替换 type 的 __call__ 运算符重载机制，“超越变形”正常的类
"""
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
