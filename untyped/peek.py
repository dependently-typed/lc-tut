class Peekable:
    def __init__(self, iter):
        self.iter = iter

        try:
            item = self.iter.__next__()
            self.peeking = item
        except StopIteration:
            self.peeking = None

        self.pointing = None

    def peek(self):
        return self.peeking

    def next(self):
        try:
            self.pointing = self.peeking
            self.peeking = self.iter.__next__()
        except StopIteration:
            self.peeking = None

        return self.pointing
