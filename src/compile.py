from src.expr import Expr
from src.lang import Num, Add1
from src.asm import Reg, Const, IMov, IAdd1
from src.asm import instruction, pprint_instrs


def compile_expr(expr: Expr, env: list) -> list[instruction]:
    match expr:
        case Num(n):
            return [IMov(Reg.RAX, Const(n))]
        case Add1(n):
            return compile_expr(n, env) + [IAdd1(Reg.RAX)]
        case _:
            raise NotImplementedError(f"Compilation not implemented for {expr}")




def compile(expr: Expr) -> str:
    instrs = compile_expr(expr, [])
    prelude = (
        "section .text\n"
        "global our_code_starts_here\n"
        "our_code_starts_here:"
    )
    return prelude + "\n" + pprint_instrs(instrs)
