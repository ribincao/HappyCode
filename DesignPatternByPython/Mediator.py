"""
author: ribincao
desc: MediatorModel Demo
"""


class User:

    def __init__(self, name):
        self.name = name

    def say(self, string):
        ChatRoomMediator.say(self, string)


class ChatRoomMediator:

    def __init__(self):
        pass

    @staticmethod
    def say(user: User, msg: str):
        print(f'{user.name}: {msg}')


if __name__ == '__main__':
    ribin = User("RibinCao")
    tommy = User("TommyLiu")
    ribin.say("hello")
    tommy.say("hi")
