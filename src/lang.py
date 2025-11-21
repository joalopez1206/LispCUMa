from lark import Lark, Transformer
from dataclasses import dataclass
from src.expr import Expr
from typing import cast

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
    var: Id
    nexpr: Expr
    body: Expr

@dataclass
class If(Expr):
    cond: Expr
    tr: Expr
    fl: Expr

@dataclass
class Fun(Expr):
    name: Id
    body: Expr

@dataclass
class App(Expr):
    fn: Expr
    args: Expr

@dataclass
class Add1(Expr):
    n: Expr

@dataclass
class Sub1(Expr):
    n: Expr

class tran(Transformer):

    def add1(self, n):
        return Add1(n[0])
    
    def sub1(self, n):
        return Sub1(n[0])

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
        return Let(n[0], n[1], n[2])
    
    def myif(self,n):
        return If(n[0],n[1],n[2])
    
    def fun(self,n):
        return Fun(n[0], n[1])
    
    def app(self,n):
        return App(n[0],n[1])
    
    def CNAME(self, n):
        return Id(n[0])
    


grammar = """?expr :  SIGNED_NUMBER -> num
        | "true" -> true
        | "false" -> false
        | name 
        | list
        
list  :   "(" "+" expr expr ")" -> add
        | "(" "-" expr expr ")" -> sub
        | "(" "add1" expr ")" -> add1
        | "(" "sub1" expr ")" -> sub1
        | "(" "let" "(" name expr ")"  expr ")" -> let
        | "(" "if" expr expr expr ")" -> myif
        | "(" "fun" "(" name+ ")" expr ")" -> fun
        | "(" expr expr ")" -> app

name  : CNAME -> var

%import common.CNAME
%import common.SIGNED_NUMBER
%import common.WS
%ignore WS"""

parser = Lark(grammar, start  = "expr", parser = "lalr", transformer = tran())

def parse(src: str) -> Expr:
    # lark's stubs type parser.parse as returning a ParseTree even when a Transformer is supplied.
    # We know the transformer returns an Expr, so cast to satisfy mypy.
    return cast(Expr, parser.parse(src))


#pprint(parse("((fun (x) (+ 2 x)) 2)"))


#pprint(parse("(fun (x) (+ 2 x))"))
#pprint(parse("(let (x 1) x)"))
#pprint(parse("""(let 
#        (x (fun (y) (+ y 1)))
#        (x 100)
#        )"""))