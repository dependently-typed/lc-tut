from .cursor import Cursor
from .peek import Peekable
from .token import *

class Lexer:
    def __init__(self, input):
        self.input = input
        self.cursor = Cursor(self.input)

    def __iter__(self):
        self.cursor = Cursor(self.input)
        return self

    def __next__(self):
        token = self._lex_token()
        if token is None:
            raise StopIteration
        return token

    def next(self):
        try:
            return self.__next__()
        except StopIteration:
            return None

    def _lex_token(self):
        self.cursor.chomp_all(is_ignored_ch)

        peek_ch = self.cursor.peek()
        if peek_ch is None:
            return None

        token = None
        if peek_ch == '@':
            token = LambdaSymbol()
            self.cursor.next()
        elif peek_ch == '(':
            token = Lparen()
            self.cursor.next()
        elif peek_ch == ')':
            token = Rparen()
            self.cursor.next()
        elif peek_ch == '.':
            token = Dot()
            self.cursor.next()
        elif peek_ch == '=':
            token = Equals()
            self.cursor.next()
        elif peek_ch.isdigit():
            token = self._lex_number()
        else:
            token = self._lex_identifier()
            if token and token.value == 'let':
                token = Let()

        if token is None:
            raise LexError(f"Invalid character '{self.cursor.peek()}'")

        self.cursor.chomp_all(is_ignored_ch)

        return token

    def _lex_number(self):
        peek_ch = self.cursor.peek()

        if not peek_ch.isdigit():
            return None
        
        num = []
        while True:
            ch = self.cursor.peek()

            if ch is None or ch.isspace():
                break

            if ch.isdigit():
                num.append(ch)
            else:
                break

            self.cursor.next()

        if len(num) == 0:
            return None
        else:
            return Nat(int(''.join(num)))

    def _lex_identifier(self):
        peek_ch = self.cursor.peek()

        if not peek_ch.isalpha() and peek_ch != '_':
            return None
        
        ident = []
        while True:
            ch = self.cursor.peek()

            if ch is None or ch.isspace():
                break

            if ch.isalpha() or ch.isdigit() or ch == '_':
                ident.append(ch)
            else:
                break

            self.cursor.next()

        if len(ident) == 0:
            return None
        else:
            return Ident(''.join(ident))

def is_ignored_ch(ch):
    return ch.isspace() or ch == ';'

class LexError(Exception):
    pass
