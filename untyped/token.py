from dataclasses import dataclass
from enum import Enum
from abc import ABC

class Token(ABC):
    value = None

    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return str(self.value)

class LambdaSymbol(Token):
    value = '@'

class Lparen(Token):
    value = '('

class Rparen(Token):
    value = ')'

class Dot(Token):
    value = '.'

class Semicolon(Token):
    value = ';'

class Equals(Token):
    value = '='

class Let(Token):
    value = 'let'

@dataclass
class Ident(Token):
    value: str
    name = "identifier"

@dataclass
class Nat(Token):
    value: int
    name = "nat"

