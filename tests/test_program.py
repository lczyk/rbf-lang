import pytest

from rbf_lang.command import Command
from rbf_lang.program import InvalidProgramError, Program, ProgramPointerError


def test_run() -> None:
    source = "*>" * 8
    program = Program(source)

    assert program == source


def test_hashable() -> None:
    source = "*>" * 8
    program = Program(source)
    hash_1 = hash(source)
    hash_2 = hash(program)

    assert hash_1 == hash_2


def test_equality() -> None:
    source = "*>" * 8
    program_1 = Program(source)
    program_2 = Program(source)

    assert program_1 == program_2


def test_move() -> None:
    source = "*>" * 8
    program = Program(source)

    assert len(program) == 16
    assert program.pointer == 0

    for i in range(15):
        assert program.pointer == i
        program.move_right()

    assert program.steps == 15

    # We now should be at the end of the program
    assert program.pointer == 15
    with pytest.raises(ProgramPointerError):
        program.move_right()

    assert program.pointer == 15
    # This still should have incremented the steps
    assert program.steps == 16

    for i in range(15, 0, -1):
        assert program.pointer == i
        program.move_left()

    assert program.pointer == 0
    assert program.steps == 31

    with pytest.raises(ProgramPointerError):
        program.move_left()

    assert program.steps == 32


def test_reset() -> None:
    source = "*>" * 8
    program = Program(source)

    program.move_right(4)

    assert program.pointer == 4
    assert program.steps == 4

    program.reset()

    assert program.pointer == 0
    assert program.steps == 0


def test_getitem() -> None:
    source = "*>" * 8
    program = Program(source)

    assert program[0] == Command("*")
    assert program[1] == Command(">")
    assert program[2] == Command("*")

    assert program[0:3] == [Command("*"), Command(">"), Command("*")]


def test_command_property() -> None:
    source = "*>" * 8
    program = Program(source)

    assert program.command == Command("*")
    program.move_right()
    assert program.command == Command(">")


def test_loop_start() -> None:
    source = "(*)*"
    program = Program(source)

    # Current bit is 0, so we should jump *past* the matching )
    program.loop_start(False)
    assert program.pointer == 3
    assert program.steps == 1

    program.reset()

    # Current bit is 1, so we should noop (but still increment steps)
    program.loop_start(True)
    assert program.pointer == 1
    assert program.steps == 1


def test_loop_start_overflow() -> None:
    source = "(*)"
    program = Program(source)

    # Current bit is 0, so we should jump *past* the matching )
    with pytest.raises(ProgramPointerError):
        program.loop_start(False)
    assert program.pointer == 2
    assert program.steps == 1

    program.reset()

    # Current bit is 1, so we should noop (but still increment steps)
    program.loop_start(True)
    assert program.pointer == 1
    assert program.steps == 1


def test_loop_start_only_on_bracket() -> None:
    source = "(*)"
    program = Program(source)
    program.move_right()

    # We're not on a loop start bracket
    with pytest.raises(ValueError):
        program.loop_start(False)


def test_loop_start_nested_brackets() -> None:
    source = "(*(*))*"
    program = Program(source)

    # Current bit is 0, so we should jump *past* the matching )
    program.loop_start(False)
    assert program.pointer == 6
    assert program.steps == 1


def test_loop_end() -> None:
    source = "(*)*"
    program = Program(source)
    program.move_right(2)

    # Current bit is 0, so we should jump back to just after the matching (
    program.loop_end(False)
    assert program.pointer == 1
    assert program.steps == 3

    program.reset()
    program.move_right(2)

    # Current bit is 1, so we should noop (but still increment steps)
    program.loop_end(True)
    assert program.pointer == 3
    assert program.steps == 3


def test_loop_end_overflow() -> None:
    source = "(*)>"
    program = Program(source)
    program.move_right(2)

    # Current bit is 0, so we should jump back to just after the matching (
    program.loop_end(False)
    assert program.pointer == 1
    assert program.steps == 3

    program.reset()
    program.move_right(2)

    # Current bit is 1, so we should noop (but still increment steps)
    program.loop_end(True)
    assert program.pointer == 3
    assert program.steps == 3


def test_loop_end_only_on_bracket() -> None:
    source = "(*)"
    program = Program(source)

    # We're not on a loop end bracket
    with pytest.raises(ValueError):
        program.loop_end(False)


def test_loop_end_nested_brackets() -> None:
    source = "(*(*))*"
    program = Program(source)
    program.move_right(5)

    program.loop_end(False)
    assert program.pointer == 1
    assert program.steps == 6


def test_invalid_program() -> None:
    source = "*)"
    with pytest.raises(InvalidProgramError):
        Program(source)


def test_copy() -> None:
    source = "*>" * 8
    program = Program(source)
    program_2 = program.copy()

    assert program == program_2
    assert program is not program_2
