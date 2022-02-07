from .peek import Peekable

class Cursor:
    def __init__(self, input):
        self.input = input
        self.cursor = Peekable(iter(self.input))

    def chomp(self, c):
        assert(self.peek() == c)
        self.next()

    def chomp_whitespace(self):
        while True:
            if self.peek() is not None and self.peek().isspace():
                next(self)
            else:
                break

    def chomp_all(self, condition):
        while True:
            if self.peek() is not None and condition(self.peek()):
                next(self)
            else:
                break

    def __iter__(self):
        self.cursor = Peekable(iter(self.input))
        return self
 
    def __next__(self):
        return self.cursor.next()

    def next(self):
        return self.cursor.next()

    def peek(self):
        return self.cursor.peek()
