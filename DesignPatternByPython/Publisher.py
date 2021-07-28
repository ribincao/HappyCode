"""
author: ribincao
desc: SimpleEventDispatcherDemo
Date: 2021/6/30
"""
from typing import Callable, Type


class Event:

    def __init__(self):
        pass


class LoginEvent(Event):
    
    def __init__(self):
        super(LoginEvent, self).__init__()


class EventDispatcher:

    def __init__(self):
        self._listen = {}

    def add_event(self, event: type, handler: Callable[[Event], None]):
        # print("add_event: ", event.__name__)
        event_name = event.__name__
        if not self._has_listener(event_name, handler):
            handlers = self._listen.get(event_name, [])
            handlers.append(handler)
            self._listen[event_name] = handlers
            # print("add listener success")
            # print(len(self._listen[event_name]))

    def _has_listener(self, event_name: str, handler: Callable[[Event], None]):
        # print("check handler: ", event_name)
        if event_name in self._listen:
            return handler in self._listen[event_name]
        return False

    def dispatch_event(self, event: Event):
        # print("dispatch_event: ", event.__class__.__name__)
        event_name = event.__class__.__name__
        if event_name in self._listen:
            handlers = self._listen[event_name]
            try:
                for handler in handlers:
                    handler()
            except Exception as error:
                print(error)


class AppMediator:

    def __init__(self, name: str, event_dispatcher: EventDispatcher):
        self.name = name
        self.event_dispatcher = event_dispatcher

    def add_event_listen(self, event_clazz: Type[Event], handler: Callable):
        self.event_dispatcher.add_event(event_clazz, handler)

    def dispatch_event(self, event: Event):
        self.event_dispatcher.dispatch_event(event)


class Entity(AppMediator):

    def __init__(self, name: str, event_dispatcher: EventDispatcher):
        super(Entity, self).__init__(name, event_dispatcher)
        self.add_event_listen(LoginEvent, self.hello)  # 添加事件

    def hello(self):
        print(f"{self.name} say hello")

    def do_something(self, event: Event):
        self.dispatch_event(event)


if __name__ == '__main__':
    eventDispatcher = EventDispatcher()

    entity1 = Entity("ribincao", eventDispatcher)
    entity2 = Entity("tommyliu", eventDispatcher)
    entity3 = Entity("allyli", eventDispatcher)

    entity1.do_something(LoginEvent())
