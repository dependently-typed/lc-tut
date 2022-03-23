from .ast import *
from abc import ABC

class Evaluator(ABC):
    bindings = {}
    fresh_name_cnt = -1

    def eval(self, expr):
        """
        Base evaluator

        Expands all free occurrences of bound terms tracked by `bindings`
        """
        
        bound_vars = set()

        def helper(expr, depth):
            result = None

            if isinstance(expr, Var):
                if expr in self.bindings and expr not in bound_vars:
                    result = self.bindings[expr]
                else:
                    result = expr
            elif isinstance(expr, Num):
                result = expr
            elif isinstance(expr, Abs):
                bound_vars.add((depth, expr.binder))
                result = Abs(
                    binder=expr.binder,
                    body=helper(expr.body, depth+1)
                )
                bound_vars.remove((depth, expr.binder))
            elif isinstance(expr, App):
                result = App(
                    func=helper(expr.func, depth+1),
                    arg=helper(expr.arg, depth+1)
                )
            elif isinstance(expr, NamedExpr):
                result = NamedExpr(
                    name=expr.name,
                    expr=helper(expr.expr, depth+1)
                )
            else:
                raise EvalError(f"eval not implemented for '{expr}'")

            return result
        
        return helper(expr, 0)

    def beta_reduce(self, e, x, y):
        """
        Perform e[x/y] (Replace all occurences of x by y in e)
    
        x must be a Var
        """
        
        if isinstance(e, Var):
            if e == x:
                return y
            else:
                return e
        elif isinstance(e, Num):
            return e
        elif isinstance(e, Abs):
            if e.binder == y:
                fresh = self.make_fresh_name(e, y)
                e = self.alpha_rename(e, y, fresh)
            elif e.binder == x:
                return e
            return Abs(
                binder=e.binder,
                body=self.beta_reduce(e.body, x, y)
            )
        elif isinstance(e, App):
            return App(
                func=self.beta_reduce(e.func, x, y),
                arg=self.beta_reduce(e.arg, x, y)
            )
        elif isinstance(e, NamedExpr):
            raise EvalError(f"beta reduction not defined for named exprs '{e}'")
        else:
            raise EvalError(f"beta reduction not implemented for '{e}'")
    
    def alpha_rename(self, e, y, fresh):
        """
        Replace all occurrences of y by fresh in e
        """
        if isinstance(e, Var):
            if e == y:
                return fresh
            else:
                return e
        elif isinstance(e, Num):
            return e
        elif isinstance(e, Abs):
            return Abs(
                binder=self.alpha_rename(e.binder, y, fresh),
                body=self.alpha_rename(e.body, y, fresh)
            )
        elif isinstance(e, App):
            return App(
                func=self.alpha_rename(e.func, y, fresh),
                arg=self.alpha_rename(e.arg, y, fresh)
            )
        else:
            raise EvalError(f"alpha_rename not implemented for '{e}'")
    
    def make_fresh_name(self, e, y):
        """
        Produce a fresh name different from the names present in e and y
        """
        
        def get_names(e, bin):
            if isinstance(e, Var):
                bin.add(e.name)
            elif isinstance(e, Abs):
                get_names(e.binder, bin)
                get_names(e.body, bin)
            elif isinstance(e, App):
                get_names(e.func, bin)
                get_names(e.arg, bin)
            else:
                raise EvalError(f"get_names not implemented for '{e}'")
    
        names = set()
        get_names(e, names)
        get_names(y, names)
    
        while True:
            self.fresh_name_cnt += 1
            fresh = f"_{self.fresh_name_cnt}"
            if fresh not in names:
                break
    
        return Var(fresh)
    
class CallByValue(Evaluator):
    def eval(self, expr):
        def helper(expr):
            if isinstance(expr, Num) or isinstance(expr, Abs) or isinstance(expr, Var):
                return expr
            elif isinstance(expr, App):
                func = helper(expr.func)
                arg = helper(expr.arg)
    
                if not isinstance(func, Abs):
                    raise EvalError(f"Expected a lambda, found '{func}'")
    
                result = self.beta_reduce(func.body, func.binder, arg)
    
                return helper(result)
            elif isinstance(expr, NamedExpr):
                body = helper(expr.expr)
                self.bindings[expr.name] = body
                return NamedExpr(
                    name=expr.name,
                    expr=body
                )
            else:
                raise EvalError(f"eval not implemented for '{expr}'")

        expr = super().eval(expr)
        return helper(expr)

class EvalError(Exception):
    pass
