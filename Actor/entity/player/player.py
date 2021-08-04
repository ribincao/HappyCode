from inteface import IPlayer
from Actor.pyactor.actor.actor import ActorBase


class Player(IPlayer, ActorBase):

    async def play(self):
        print("play")

    async def echo(self):
        print("echo")
