


from typing import Optional


class Product:

    def __init__(self):
        pass


class Product1(Product):

    def __init__(self):
        super(Product1, self).__init__()
        print("Product1")


class Product2(Product):

    def __init__(self):
        super(Product2, self).__init__()
        print("Product2")


class SimpleFactory:

    def __init__(self):
        pass

    @staticmethod
    def create_product(name: int) -> Optional[Product]:
        if name == 1:
            return Product1()
        if name == 2:
            return Product2()
        return None


if __name__ == '__main__':
    sf = SimpleFactory()
    p1 = sf.create_product(1)
    p2 = sf.create_product(2)
