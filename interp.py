from lang import Fun, App, Expr, Add, Sub, Num, Bool, Id, parse, If
from env import Val, NumV, BoolV, ClosureV
from env import lookup, Env

def interp(expr: Expr, env: Env) -> Val:
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
            return interp(l, env) + interp(r, env)
        case Sub(l,r):
            return interp(l, env) - interp(r, env)
        case If(c, t, f):
            if interp(c, env) == BoolV(True):
                return interp(t, env)
            else:
                return interp(f, env)
        case App(fexpr, argexpr):
            closure = interp(fexpr, env)
            if not isinstance(closure, ClosureV):
                raise TypeError("Not a Closure!")
            idx = closure.name
            body = closure.body
            fenv = closure.env
            return interp(body, fenv.extend(idx.name, interp(argexpr, env)))
        case _:
            raise TypeError("Not defined!")

def compile(expr: Expr):
    ...

def run(src: str) -> int:
    return interp(parse(src), Env([]))
# "(let (x 1) x)"

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
           )""" )== NumV(101)

try:
    run("(let (x y) x)")
except ValueError:
    print("Test good!")

