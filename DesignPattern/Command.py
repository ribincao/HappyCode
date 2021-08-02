"""
author: ribincao
desc: CommandModel Demo
"""
from typing import List


class Command:

    def __init__(self):
        self.name = "ribincao"

    def buy(self):
        print(f'{self.name} buy something.')

    def sell(self):
        print(f"{self.name} sell something.")

    def execute(self):
        pass


class BuyCommand(Command):

    def __init__(self):
        super(BuyCommand, self).__init__()

    def execute(self):
        self.buy()


class SellCommand(Command):

    def __init__(self):
        super(SellCommand, self).__init__()

    def execute(self):
        self.sell()


class CommandMaker:

    def __init__(self):
        self.commands: List[Command] = list()

    def add_command(self, command: Command):
        self.commands.append(command)

    def execute(self):
        if self.commands:
            for command in self.commands:
                command.execute()
        self.commands.clear()


if __name__ == '__main__':
    cm = CommandMaker()
    cm.add_command(SellCommand())
    cm.add_command(BuyCommand())
    # print(len(cm.commands))
    cm.execute()
    # print(len(cm.commands))

