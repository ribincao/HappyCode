"""
author: ribincao
desc: ProxyModel Demo
"""


class PersonImp:

    def __init__(self):
        pass

    def hello(self):
        pass


class Person(PersonImp):

    def __init__(self, name):
        self.name = name
        super(Person, self).__init__()
        pass

    def hello(self):
        print(f'{self.name} say hello')


class PersonProxy(PersonImp):

    def __init__(self, name):
        super(PersonProxy, self).__init__()
        self.name = name
        self._person = None

    def hello(self):
        if not self._person:
            self._person = Person(self.name)
        self._person.hello()


if __name__ == '__main__':
    pp = PersonProxy("ribincao")
    pp.hello()