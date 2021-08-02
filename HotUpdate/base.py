a = 1


def incr(x):
    tmp = 1
    return x + tmp


class Test:

    def __init__(self, name):
        self.name = name

    def hello(self):
        print(f"{self.name} say hello")

    @staticmethod
    def hi():
        print("hi")
