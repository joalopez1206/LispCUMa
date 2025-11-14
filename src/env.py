from dataclasses import dataclass
from expr import Expr

class Val:
    ...


@dataclass
class Env:
    env : list[tuple[str, Val]]

    def extend(self, id, val) -> "Env":
        return Env([(id, val)] + self.env)
    
def lookup(s :str, env: Env) -> Val :
    match env.env:
        case []:
            raise ValueError("Free Identifier!")
        case [(x, e), *xs]:
            return e if x==s else lookup(s, Env(xs)) 

@dataclass
class NumV(Val):
    n: int
    def __add__(self, other):
        if isinstance(other, NumV):
            return NumV(self.n + other.n)
        else:
            raise TypeError("Not defined!")
    
    def __sub__(self, other):
        if isinstance(other, NumV):
            return NumV(self.n - other.n)
        else:
            raise TypeError("Not defined!")

@dataclass
class BoolV(Val):
    b: bool

@dataclass
class ClosureV(Val):
    name: str
    body: Expr
    env: Env


