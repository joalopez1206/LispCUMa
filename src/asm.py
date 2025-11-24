from enum import auto, Enum
from dataclasses import dataclass

class Reg(Enum):
    RAX = auto()
    RSP = auto()

@dataclass
class Const:
    value: int

@dataclass
class RegOffset:
    reg: Reg
    offset: int

type arg = Const | Reg | RegOffset

def arg_to_str(a: arg) -> str:
    match a:
        case Const(value):
            return str(value)
        case Reg() as reg:
            return reg.name
        case RegOffset(reg, offset):
            return f"[{reg.name} - 8*{offset}]"
        case _:
            raise TypeError("Unknown arg type")

class IRet:
    def __str__(self) -> str:
        return "  ret"

@dataclass
class IAdd:
    left: arg
    right: arg

    def __str__(self):
        return f"  add {arg_to_str(self.left)} ,{arg_to_str(self.right)}"

@dataclass
class IMov:
    dst: arg
    src: arg

    def __str__(self) -> str:
        return f"  mov {arg_to_str(self.dst)}, {arg_to_str(self.src)}"

@dataclass
class IAdd1:
    dst: arg

    def __str__(self) -> str:
        return f"  add {arg_to_str(self.dst)}, 1"


type instruction = IRet | IMov | IAdd1 | IAdd 

def pprint_instrs(instrs: list[instruction]) -> str:
    return "\n".join(str(instr) for instr in instrs)