from .repl import startrepl
from .eval import CallByValue
from .utlc import eval_file
from .ast import NamedExpr
import sys

def main():
    evaluator = CallByValue()
    if len(sys.argv) == 1:
        startrepl(evaluator)
    else:
        filenames = sys.argv[1:]
        for file in filenames:
            results = eval_file(evaluator, file)

            for result in results:
                if isinstance(result, NamedExpr) and result.name.name == "main":
                    print(result.expr)
                    break

if __name__ == "__main__":
    main()
