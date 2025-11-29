from src.expr import Expr
from src.lang import Num, Add1, Let, Id, Add
from src.asm import Reg, Const, IMov, IAdd1, IRet, RegOffset, IAdd
from src.asm import instruction, pprint_instrs


type compEnv = list[tuple[str, int]]


class Gensym:
    def __init__(self, s: str):
        self.s = s
        self.i = 0

    def gen(self) -> str:
        s = f"{self.s}{self.i}"
        self.i += 1
        return s


gensym = Gensym("x")


def add(env: compEnv, name: str) -> tuple[compEnv, int]:
    i = 1 + len(env)
    return [(name, i)] + env, i


def lookup(env: compEnv, s: str):
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
        case Add(l, r):
            lsym = gensym.gen()
            rsym = gensym.gen()
            en1, loffset = add(env, lsym)
            en2, roffset = add(en1, rsym)

            left_instr = compile_expr(l, en2)
            lstack = [IMov(RegOffset(Reg.RSP, loffset), Reg.RAX)]
            right_instr = compile_expr(r, en2)
            rstack = [IMov(RegOffset(Reg.RSP, roffset), Reg.RAX)]
            leave_res_in_rax = [IMov(Reg(Reg.RAX), RegOffset(Reg.RSP, loffset))]

            return (
                left_instr
                + lstack
                + right_instr
                + rstack
                + leave_res_in_rax
                + [IAdd(Reg.RAX, RegOffset(Reg.RSP, roffset))]
            )
        case Let(var, nexpr, body):
            nenv, slot = add(env, var.name)
            instrs = compile_expr(nexpr, env)
            return (
                instrs
                + [IMov(RegOffset(Reg.RSP, slot), Reg.RAX)]
                + compile_expr(body, nenv)
            )
        case _:
            raise NotImplementedError(f"Compilation not implemented for {expr}")


def compile(expr: Expr) -> str:
    instrs = compile_expr(expr, [])
    prelude = "section .text\nglobal our_code_starts_here\nour_code_starts_here:"
    return prelude + "\n" + pprint_instrs(instrs + [IRet()])
