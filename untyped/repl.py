import readline
from .utlc import eval, expand, eval_file

prompt = ">> "
help_msg = """
:quit                       Quit the repl
:expand <expr>              Print expression after term expansion
:load <file> [<file> ...]   Load definitions from a file
:help                       Show this message
"""

def startrepl(evaluator):
    print("==untyped lambda calculus==")
    print("type ':quit' to quit this session")
    print("type ':help' for help")

    def get_cmd(inp):
        idx = inp.find(' ')
        if idx == -1:
            idx = len(inp)
    
        return inp[1:idx], inp[idx:]
    
    while True:
        inp = input(prompt)

        if len(inp) == 0:
            continue

        if inp[0] == ':':
            cmd, rest = get_cmd(inp)
            if cmd == 'quit':
                exit(0)
            elif cmd == 'expand':
                for e in expand(evaluator, rest):
                    print(":~", e)
            elif cmd == 'help':
                print(help_msg)
            elif cmd == 'load':
                filenames = rest.strip().split(' ')
                for file in filenames:
                    eval_file(evaluator, file)
            else:
                print(f"[repl error] Invalid command ':{cmd}'")
        else:
            for e in eval(evaluator, inp):
                print(":-", e) 
