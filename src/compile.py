from src.expr import Expr
from src.lang import Num, Add1, Let, Id
from src.asm import Reg, Const, IMov, IAdd1, IRet, RegOffset
from src.asm import instruction, pprint_instrs
from dataclasses import dataclass


type compEnv =  list[tuple[str, int]]

def add(env: compEnv, name: str) -> compEnv:
    i = len(env)
    return [(name, i)] + env

def lookup(env: compEnv, s:str):
    match env:
        case [(a, i), *xs]:
            return i if a == s else lookup(xs, s)
        case _:
            raise ValueError()

def compile_expr(expr: Expr, env: compEnv) -> list[instruction]:
    match expr:
        case Id(x):
            offset = lookup(env, x)
            return [IMov(Reg.RAX, RegOffset(Reg.RSP, offset))]
        case Num(n):
            return [IMov(Reg.RAX, Const(n))]
        case Add1(n):
            return compile_expr(n, env) + [IAdd1(Reg.RAX)]
        case Let(var, nexpr, body):
            nenv = add(env, var.name)
            instrs = compile_expr(nexpr, env)
            return instrs + compile_expr(body, nenv)
        case _:
            raise NotImplementedError(f"Compilation not implemented for {expr}")




def compile(expr: Expr) -> str:
    instrs = compile_expr(expr, [])
    prelude = (
        "section .text\n"
        "global our_code_starts_here\n"
        "our_code_starts_here:"
    )
    return prelude + "\n" + pprint_instrs(instrs + [IRet()])
