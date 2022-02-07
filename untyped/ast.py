from dataclasses import dataclass
from abc import ABC

class AstNode(ABC):
    pass

class ValueNode(AstNode):
    pass

@dataclass
class Var(ValueNode):
    name: str

    def __str__(self):
        return self.name

@dataclass
class Num(ValueNode):
    val: int

    def __str__(self):
        return str(self.val)

@dataclass
class Abs(ValueNode):
    binder: Var
    body: AstNode

    def __str__(self):
        return f"(@{str(self.binder)}. {str(self.body)})"

@dataclass
class App(AstNode):
    func: AstNode
    arg: AstNode

    def __str__(self):
        return f"({str(self.func)} {str(self.arg)})"

@dataclass
class NamedExpr(AstNode):
    name: str
    expr: AstNode

    def __str__(self):
        return f"let {self.name} = {str(self.expr)}"
