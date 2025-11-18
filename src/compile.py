from src.expr import Expr
from typing import Protocol

class Instructions(Protocol):
    ...

def compile_expr(expr: Expr, env: list) -> list[Instructions]:
    return []


def pprint_instrs(instrs: list[Instructions]) -> str:
    return "\tmov RAX, 0\n\tret"

def compile(expr: Expr) -> str:
    instrs = compile_expr(expr, [])
    prelude = (
        "section .text\n"
        "global our_code_starts_here\n"
        "our_code_starts_here:"
    )
    return prelude + "\n" + pprint_instrs(instrs)
