from src.lang import Fun, App, Expr, Add, Sub, Num, Bool, Id, parse, If
from src.env import Val, NumV, BoolV, ClosureV
from src.env import lookup, Env

def interp_expr(expr: Expr, env: Env) -> Val:
    match expr:
        case Id(x):
            return lookup(x, env)
        case Fun(name, body):
            return ClosureV(name, body, env)
        case Num(n):
            return NumV(n)
        case Bool(b):
            return BoolV(b)
        case Add(l,r):
            match (interp_expr(l, env),interp_expr(r, env)):
                case (NumV() as left, NumV() as right):
                    return left+right
                case _:
                    raise TypeError("Not a Number!")
        case Sub(l,r):
            match (interp_expr(l, env),interp_expr(r, env)):
                case (NumV() as left, NumV() as right):
                    return left-right
                case _:
                    raise TypeError("Not a Number!")
        case If(c, t, f):
            match interp_expr(c, env):
                case BoolV(b):
                    return interp_expr(t, env) if b else interp_expr(f, env)
                case _:
                    raise TypeError("Not a Boolean!")
        case App(fexpr, argexpr):
            closure = interp_expr(fexpr, env)
            if not isinstance(closure, ClosureV):
                raise TypeError("Not a Closure!")
            idx = closure.name
            body = closure.body
            fenv = closure.env
            return interp_expr(body, fenv.extend(idx.name, interp_expr(argexpr, env)))
        case _:
            raise TypeError("Not defined!")

def interp(src: Expr) -> Val:
    return interp_expr(src, Env([]))

def run(src: str) -> Val:
    return interp_expr(parse(src), Env([]))
 
