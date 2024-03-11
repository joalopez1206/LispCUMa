from interp import run
from lang import Val, NumV, BoolV

def print_val(v: Val):
    match v:
        case NumV(n):
            print(str(n))
        case BoolV(b):
            print(str(b))
        case _:
            raise ValueError("Not defined!")

def main():
    print("Lisp CUMa")
    while True:
        try:
            s = input(">> ")
            print_val(run(s))
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except BaseException as e:
            print(e)

if __name__ == "__main__":
    main()