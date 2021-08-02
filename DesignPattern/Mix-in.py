class Animal:
    
    def __init__(self, name):
        print("Animal")
        self.name = name

    def eat(self):
        print(f"{self.name} eat")

    def sleep(self):
        print(f"{self.name} sleep")


class AnimalMixin:
    """
    Mixin 类应该表示某种单一的功能且不依赖子类的实现, 子类没有 mixin 累也可已正常工作, 比如:
        交通工具(基类) + 天上飞Mixin + 地上跑Mixin + 海里漂Mixin
    """
    def __init__(self):
        print("Animal Mixin")

    def make_tools(self):
        print(f"{self.name} make tools")


class Person(Animal, AnimalMixin):
    """
    AnimalMixin 的构造函数不会被调用
    """
    def __init__(self, name):
        """
        方法顺序解释(MRO): Person -> Animal -> AnimalMixin
        """
        super(Person, self).__init__(name)

    def power(self):
        super(Person, self).make_tools()


if __name__ == '__main__':
    p = Person("ribincao")
    p.eat()
    p.sleep()
    p.power()