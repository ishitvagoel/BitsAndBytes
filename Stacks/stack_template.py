'''Repl.it : https://repl.it/@Ishitva/StackTemplate'''

class StackFullException(Exception):
    pass

class StackEmptyException(Exception):
    pass


def checkStackFull(func):
    def execute(self, *args, **kwargs):
        if len(self.items) < self.limit:
            return func(self, *args, **kwargs)
        raise StackFullException()

    return execute


def checkStackEmpty(func):
    def execute(self, *args, **kwargs):
        if len(self.items):
            return func(self, *args, **kwargs)
        raise StackEmptyException()
    return execute


class Stack():
    def __init__(self, limit=10):
        self.items = []
        self.limit = limit

    @checkStackFull
    def push(self, item):
        self.items.append(item)
        return item

    @checkStackEmpty
    def pop(self):
        return self.items.pop()

    def getSize(self):
        return len(self.items)

    @checkStackEmpty
    def peek(self):
      return self.items[-1]