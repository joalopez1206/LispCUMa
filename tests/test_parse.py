from src.lang import parse, Num, Add, Bool
def test_num():
    assert parse("1") == Num(1)

def test_add():
    assert parse("(+ 1 2)") == Add(Num(1), Num(2))

def test_add_nested():
    assert parse("(+ 1 (+ 2 3))") == Add(Num(1), Add(Num(2), Num(3)))

def test_bools():
    assert parse("true") == Bool(True)
    assert parse("false") == Bool(False)
    assert parse("false") != Bool(True)