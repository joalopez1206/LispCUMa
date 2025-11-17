from src.interp import run
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 run_interp.py <filename>")