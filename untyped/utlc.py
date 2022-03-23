from .lexer import Lexer, LexError
from .parser import Parser, ParseError
from .eval import Evaluator, EvalError

def get_exprs(inp):
    try:
        lexer = Lexer(inp)
        parser = Parser(lexer)
        exprs = parser.parse()
        return [expr for expr in exprs if expr is not None]
    except ParseError as e:
        print("[parse error]", e)
    except LexError as e:
        print("[lex error]", e)
    return []

def eval(evaluator, inp):
    try:
        return [
            evaluator.eval(expr)
            for expr in get_exprs(inp)
            if expr is not None
        ]
    except EvalError as e:
        print("[eval error]", e)
    return []
 
def expand(evaluator, inp):
    try:
        return [
            Evaluator.eval(evaluator, expr)
            for expr in get_exprs(inp)
            if expr is not None
        ]
    except EvalError as e:
        print("[expand error]", e)
    return []

def eval_file(evaluator, filename):
    try:
        with open(filename, 'r') as f:
            data = f.read()
            results = eval(evaluator, data)
        return results
    except Exception as e:
        print("[eval error]")
    return []
