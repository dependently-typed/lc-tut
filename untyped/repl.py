import readline
from .eval import Evaluator, CallByValue, EvalError
from .lexer import Lexer, LexError
from .parser import Parser, ParseError

prompt = ">> "

def startrepl():
    print("==untyped lambda calculus==")
    print("type ':quit' to quit this session")

    def get_cmd(inp):
        idx = inp.find(' ')
        if idx == -1:
            idx = len(inp)
    
        return inp[1:idx], inp[idx:]
    
    def get_exprs(inp):
        lexer = Lexer(inp)
        parser = Parser(lexer)
        exprs = parser.parse()
        return [expr for expr in exprs if expr is not None]
    
    def eval_exprs(exprs):
        for expr in exprs:
            result = evaluator.eval(expr)
            print(":-", result)

    def expand_exprs(exprs):
        for expr in exprs:
            result = Evaluator.eval(evaluator, expr)
            print("::-", result)

    evaluator = CallByValue()

    while True:
        inp = input(prompt)

        if len(inp) == 0:
            continue

        try:
            if inp[0] == ':':
                cmd, inp_exprs = get_cmd(inp)
                if cmd == 'quit':
                    exit(0)
                elif cmd == 'expand':
                    expand_exprs(get_exprs(inp_exprs))
                else:
                    print(f"[repl error] Invalid command ':{cmd}'")
            else:
                eval_exprs(get_exprs(inp))
        except ParseError as e:
            print("[parse error]", e)
        except LexError as e:
            print("[lex error]", e)
        except EvalError as e:
            print("[eval error]", e)
