from dataclasses import dataclass
from src.expr import Expr
from src.lang import Id
from typing import Protocol

class Val(Protocol):
    ...


@dataclass
class Env:
    env : list[tuple[str, Val]]

    def extend(self, id: str, val) -> "Env":
        return Env([(id, val)] + self.env)
    
def lookup(s :str, env: Env) -> Val :
    match env.env:
        case [(x, e), *xs]:
            return e if x==s else lookup(s, Env(xs)) 
        case [] | _:
            raise ValueError("Free Identifier!")
        
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
    name: Id
    body: Expr
    env: Env


