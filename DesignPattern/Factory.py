from SimpleFactory import *


class Factory:

    def __init__(self):
        pass


class Product1Factory(Factory):

    def __init__(self):
        super(Product1Factory, self).__init__()

    @staticmethod
    def create_product():
        return Product1()


class Product2Factory(Factory):

    def __init__(self):
        super(Product2Factory, self).__init__()

    @staticmethod
    def create_product():
        return Product2()


if __name__ == '__main__':
    pf = Product1Factory()
    p = pf.create_product()
