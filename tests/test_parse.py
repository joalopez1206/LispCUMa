from src.lang import Fun, parse, Num, Add, Bool, If, Sub, App, Id
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

def test_sub():
    assert parse("(- 3 (+ 1 2))") == Sub(Num(3), Add(Num(1), Num(2)))

def test_if():
    assert parse("(if true 1 2)") == If(Bool(True), Num(1), Num(2))
    assert parse("(if false 1 2)") == If(Bool(False), Num(1), Num(2))

def test_if_nested():
    assert parse("(if true (+ 1 2) (- 3 4))") == If(Bool(True), Add(Num(1), Num(2)), Sub(Num(3), Num(4)))

def test_let_app():
    assert parse("(let (x 1) x)") == App(
        Fun(Id("x"), Id("x")),
        Num(1)
    )

def test_let_app_add():
    assert parse("(let (x (+ 1 2)) x)") == App(
        Fun(Id("x"), Id("x")),
        Add(Num(1), Num(2))
    )

def test_let_app_nested():
    assert parse("(let (x 1) (let (y 2) (+ x y)))") == App(
        Fun(Id("x"),
            App(
                Fun(Id("y"),
                    Add(Id("x"), Id("y"))
                ),
                Num(2)
            )
        ),
        Num(1)
    )
    