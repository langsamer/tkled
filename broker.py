from collections import deque, namedtuple

__all__ = [
    'InternalEvent',
    'Broker',
]

InternalEvent = namedtuple('InternalEvent', ['name', 'data'])


class Broker(deque):
    def __init__(self, maxsize=50, event_generate=None):
        super().__init__([], maxsize)
        self.event_generate = event_generate or (lambda *args: None)

    def write(self, name, *args):
        self.append(InternalEvent(name, args))
        self.event_generate('<<SENT_EVENT>>', when='tail')

    def read(self):
        return self.popleft()
