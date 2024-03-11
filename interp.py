from dataclasses import dataclass
from lang import Expr, Add, Sub, Num, Bool,Let, Id, parse, Val, NumV, BoolV, If

@dataclass
class Env:
    amb : list[tuple[str, Val]]

def lookup(s :str, env: Env) -> Val :
    match env.amb:
        case []:
            raise ValueError("Free Identifier!")
        case [(x, e), *xs]:
            return e if x==s else lookup(s, Env(xs)) 

def interp(expr: Expr, env: Env) -> Val:
    match expr:
        case Id(x):
            return lookup(x, env)
        case Num(n):
            return NumV(n)
        case Bool(b):
            return BoolV(b)
        case Add(l,r):
            return interp(l, env) + interp(r, env)
        case Sub(l,r):
            return interp(l, env) - interp(r, env)
        case Let(i, e, b):
            v = interp(e, env)
            new_env = Env([(i.name, v)] + env.amb)
            return interp(b, new_env)
        case If(c, t, f):
            if interp(c, env) == BoolV(True):
                return interp(t, env)
            else:
                return interp(f, env)
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

try:
    run("(let (x y) x)")
except ValueError:
    print("Test good!")

