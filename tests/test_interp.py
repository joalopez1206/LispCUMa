import pytest
from src.interp import run
from src.env import NumV, BoolV, ClosureV, Env
from src.lang import Id, Add, Num

def test_arithmetic():
    assert run("1") == NumV(1)
    assert run("(+ 1 2)") == NumV(3)
    assert run("(+ 1 (+ 2 3))") == NumV(6)
    assert run("(- 3 (+ 1 2))") == NumV(0)

def test_booleans():
    assert run("true") == BoolV(True)
    assert run("false") == BoolV(False)

def test_let_bindings():
    assert run("(let (x 1) x)") == NumV(1)
    assert run("(let (x (+ 1 1)) x)") == NumV(2)

def test_if_expressions():
    assert run("(if true 1 2)") == NumV(1)
    assert run("(if false 1 2)") == NumV(2)
    assert run("(if false true false)") == BoolV(False)
    assert run("(if true false true)") == BoolV(False)
    assert run("(if false 1 (+ 1 2))") == NumV(3)
    assert run("(if true (+ 1 2) 1)") == NumV(3)

def test_functions_and_application():
    assert run("(fun (x) (+ 2 x))") == ClosureV(Id("x"), Add(Num(2), Id("x")), Env([]))
    assert run("((fun (x) (+ 2 x)) 2)") == NumV(4)
    assert run("""(let 
               (x (fun (y) (+ y 1)))
               (x 100)
               )""") == NumV(101)
    

def test_shadowing():
    assert run("""
        (let (x 1)
            (let (x 2)
                x
            )
        )
    """) == NumV(2)

def test_invalid_lookup_raises():
    with pytest.raises(ValueError):
        run("(let (x y) x)")

def test_invalid_if_condition_raises():
    with pytest.raises(TypeError):
        run("(if 1 2 3)")

def test_invalid_addition_raises():
    with pytest.raises(TypeError):
        run("(+ true 1)")

def test_invalid_subtraction_raises():
    with pytest.raises(TypeError):
        run("(- 1 false)")

def test_invalid_lookup_lexical_scope():
    with pytest.raises(ValueError):
        run("""(let 
            (y 
                (let (x 1) x))
             x)""")