import readline
from .eval import eval
from .lexer import Lexer, LexError
from .parser import Parser, ParseError

prompt = ">> "

def startrepl():
    print("==untyped lambda calculus==")
    print("type ':quit' to quit this session")

    while True:
        inp = input(prompt)
        
        if inp == ':quit':
            exit(0)

        if len(inp) == 0:
            continue

        try:
            lexer = Lexer(inp)
            parser = Parser(lexer)
            ast = parser.parse()
            
            # TODO replace this with evaluated output
            for expr in ast:
                print(expr)
        except ParseError as e:
            print("[parse error]", e)
        except LexError as e:
            print("[lex error]", e)
