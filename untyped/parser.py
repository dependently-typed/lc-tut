from .ast import *
from .token import *
from .peek import Peekable

class Parser:
    def __init__(self, lexer):
        self.lexer = Peekable(iter(lexer))

    def parse(self):
        tok = self.lexer.peek()

        if isinstance(tok, Let):
            return self.parse_named_exprs()
        else:
            return [self.parse_exprs()]

    def parse_named_exprs(self):
        named_exprs = []
        while self.lexer.peek():
            named_exprs.append(self.parse_named_expr())
        return named_exprs

    def parse_named_expr(self):
        self.chomp(Let)
        name = Var(self.chomp(Ident).value)
        self.chomp(Equals)
        expr = self.parse_exprs_until(lambda tok: isinstance(tok, Let))
        return NamedExpr(name, expr)

    def parse_expr(self):
        tok = self.lexer.peek()

        if isinstance(tok, LambdaSymbol):
            return self.parse_abs()
        
        if isinstance(tok, Ident):
            self.lexer.next()
            return Var(tok.value)

        if isinstance(tok, Nat):
            self.lexer.next()
            return Num(tok.value)

        if isinstance(tok, Lparen):
            self.lexer.next()
            expr = self.parse_exprs_until(is_boundary_tok)
            self.chomp(Rparen)
            return expr

        raise ParseError(f"Unexpected token: {tok}")

    def parse_exprs(self):
        return self.parse_exprs_until(lambda _tok: False)

    def parse_exprs_until(self, condition):
        exprs = []

        while True:
            tok = self.lexer.peek()
            if not tok or condition(tok):
                break
            exprs.append(self.parse_expr())

        if len(exprs) >= 2:
            root = App(exprs[0], exprs[1])
            for e in exprs[2:]:
                root = App(root, e)
            return root
        elif len(exprs) == 1:
            return exprs[0]
        else:
            return None

    def parse_abs(self):
        self.chomp(LambdaSymbol)
        binder = Var(self.chomp(Ident).value)
        self.chomp(Dot)
        body = self.parse_exprs_until(is_boundary_tok)
        return Abs(binder, body)

    def chomp(self, ty, msg_hint=None):
        tok = self.lexer.next()

        if not isinstance(tok, ty):
            if ty.value:
                expected = ty.value
            elif ty.name:
                expected = ty.name
            else:
                expected = ty
            raise ParseError(f"Expected '{expected}' but found '{tok}'")

        return tok

def is_boundary_tok(tok):
    return isinstance(tok, Let) or isinstance(tok, Rparen)

class ParseError(Exception):
    pass
