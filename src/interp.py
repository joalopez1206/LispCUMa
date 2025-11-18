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
            if interp_expr(c, env) == BoolV(True):
                return interp_expr(t, env)
            else:
                return interp_expr(f, env)
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
 

if __name__ == "__main__":
    assert run("1") == NumV(1)
    assert run("(+ 1 2)") == NumV(3)
    assert run("(+ 1 (+ 2 3))") == NumV(6)
    assert run("(- 3 (+ 1 2))") == NumV(0)
    assert run("true") == BoolV(True)
    assert run("false") == BoolV(False)
    assert run("(let (x 1) x)") == NumV(1)
    assert run("(let (x (+ 1 1)) x)") == NumV(2)
    assert run ("(if true 1 2)") == NumV(1)
    assert run ("(if false 1 2)") == NumV(2)
    assert run ("(if false true false)") == BoolV(False)
    assert run ("(if true false true)") == BoolV(False)
    assert run ("(if false 1 (+ 1 2))") == NumV(3)
    assert run ("(if true (+ 1 2) 1)") == NumV(3)
    assert run("(fun (x) (+ 2 x))") == ClosureV(Id("x"), Add(Num(2), Id("x")), Env([]))
    assert run ("((fun (x) (+ 2 x)) 2)") == NumV(4)
    assert run("""(let 
               (z (fun (y) (+ y 1)))
               (x 100)
               )""") == NumV(101)

    try:
        run("(let (x y) x)")
    except ValueError:
        print("Test good!")

