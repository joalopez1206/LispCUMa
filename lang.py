from lark import Lark, Transformer
from dataclasses import dataclass
from expr import Expr
from pprint import pprint

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
class If(Expr):
    cond: Expr
    tr: Expr
    fl: Expr

@dataclass
class Fun(Expr):
    name: str
    body: Expr

@dataclass
class App(Expr):
    fn: Expr
    args: Expr

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
        return App(Fun(n[0], n[2]), n[1])
    
    def myif(self,n):
        return If(n[0],n[1],n[2])
    
    def fun(self,n):
        return Fun(n[0], n[1])
    
    def app(self,n):
        return App(n[0],n[1])
    
    def CNAME(self, n):
        return Id(n[0])
    


grammar = ""

with open("grammar.lark", "r") as f:
    grammar = f.read()

parser = Lark(grammar, start  = "expr", parser = "lalr", transformer = tran())
parse = parser.parse

pprint(parse("((fun (x) (+ 2 x)) 2)"))
pprint(parse("(fun (x) (+ 2 x))"))
pprint(parse("(let (x 1) x)"))
pprint(parse("""(let 
           (x (fun (y) (+ y 1)))
           (x 100)
           )"""))