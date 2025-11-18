import sys
import os
from src.lang import parse
from src.compile import compile

if __name__ == "__main__":
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        with open(sys.argv[1]) as f:
            src = f.read()
        expr = parse(src)
        print(compile(expr))
    else:
        print("usage: run_compile.py <filename>")