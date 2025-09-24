import pytest

from rbf_lang import Program, reverse_program, run


@pytest.fixture
def move_right() -> Program:
    source = """
    # Move the bit under the pointer to the right, using a temporary cell
    # x=?, y=0, f=0
    (>>*<<) # set f if x is set
    >>( # if f is set
        <(>*<)* # set y
        <*(>>*<<) # unset x
    >>)
    <(>*<) # if y is set, unset f
    (>>*<<)>>(<(>*<)*<*(>>*<<)>>)<(>*<)
    (>>*<<)>>(<(>*<)*<*(>>*<<)>>)<(>*<)
    (>>*<<)>>(<(>*<)*<*(>>*<<)>>)<(>*<)
    """
    return Program(source)


@pytest.fixture
def move_left(move_right: Program) -> Program:
    return reverse_program(move_right)


def test_move_bit(move_right: Program) -> None:
    program, tape = run(move_right, "100")

    assert program.steps == 100
    assert tape == "010"
    program.reset()
    program, tape = run(program, tape)

    assert program.steps == 100
    assert tape == "001"


def test_move_left(move_left: Program) -> None:
    program, tape = run(move_left, "001")

    assert program.steps == 100
    assert tape == "010"

    program.reset()

    program, tape = run(program, tape)

    assert program.steps == 100
    assert tape == "100"
