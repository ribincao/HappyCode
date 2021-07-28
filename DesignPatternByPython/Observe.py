"""
author: ribincao
desc: ObserverModel Demo
"""


class User:

    def __init__(self, name):
        self.hp = 100
        self.name = name
        self.observers = list()

    def send_notification(self, hp):
        if self.observers:
            for observer in self.observers:
                observer.update(hp)


class Observer:

    def __init__(self, user):
        self.user = user


class HPObserver(Observer):

    def __init__(self, user):
        super(HPObserver, self).__init__(user)
        self.user = user
        self.user.attach(self)

    def update(self, hp):
        print(f'{self.user.name} be attacked, {hp} hp decreased.')


class Player(User):

    def __init__(self, name):
        super(Player, self).__init__(name)

    def attach(self, observer):
        self.observers.append(observer)

    def be_attack(self, hp):
        self.hp -= hp
        self.send_notification(hp)


if __name__ == '__main__':
    ribin = Player('ribincao')
    hpOb = HPObserver(ribin)
    ribin.be_attack(50)