from lark import Lark, Transformer
from dataclasses import dataclass

class Val:
    ...

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

class Expr:
    ...

@dataclass
class Num(Expr):
    val: int

@dataclass 
class Id(Expr):
    name: str

@dataclass
class Bool(Expr):
    b: bool

@dataclass
class Add(Expr):
    l: Expr
    r: Expr

@dataclass
class Sub(Expr):
    l: Expr
    r: Expr

@dataclass
class Let(Expr):
    id: str
    val: Expr
    body: Expr

@dataclass
class If(Expr):
    cond: Expr
    tr: Expr
    fl: Expr


class tran(Transformer):
    def name(self, n):
        return Id(n)
    
    def var(self,n):
        return n[0]

    def add(self, n):
        return Add(n[0],n[1])

    def sub(self, n):
        return Sub(n[0],n[1])

    def num(self, n):
        return Num(int(n[0]))
    
    def true(self, n):
        return Bool(True)
    
    def false(self, n):
        return Bool(False)
    
    def let(self, n):
        return Let(n[0],n[1],n[2])
    
    def myif(self,n):
        return If(n[0],n[1],n[2])
    
    def CNAME(self, n):
        return Id(n[0])
    

grammar = ""

with open("grammar.lark", "r") as f:
    grammar = f.read()

parser = Lark(grammar, start  = "expr", parser = "lalr", transformer = tran())
parse = parser.parse

