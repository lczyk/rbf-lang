import pytest

from rbf_lang.tape import Tape


@pytest.fixture
def tape() -> Tape:
    return Tape(8)


def test_tape(tape: Tape) -> None:
    assert len(tape) == 8
    assert tape.pointer == 0
    assert tape.tape == [False] * 8


def test_getitem(tape: Tape) -> None:
    assert tape[0] is False
    assert tape[1] is False
    assert tape[0:2] == [False, False]


def test_copy(tape: Tape) -> None:
    tape_2 = tape.copy()
    assert tape == tape_2
    assert tape is not tape_2

    tape_3 = Tape(tape)
    assert tape == tape_3
    assert tape is not tape_3


def test_hashable(tape: Tape) -> None:
    tape_2 = tape.copy()
    assert hash(tape) == hash(tape_2)
    assert hash(tape) == hash("00000000")


def test_alternative_inits() -> None:
    tape = Tape([1, 0, 1, 0, 1, 0, 1, 0])
    assert tape == "10101010"
    assert tape == [1, 0, 1, 0, 1, 0, 1, 0]

    tape = Tape("10101010")
    assert tape == "10101010"
    assert tape == [1, 0, 1, 0, 1, 0, 1, 0]


def test_toggle(tape: Tape) -> None:
    assert tape[0] is False
    tape.toggle()
    assert tape[0] is True
    tape.toggle()
    assert tape[0] is False


def test_move(tape: Tape) -> None:
    assert len(tape) == 8
    assert tape.pointer == 0

    for i in range(7):
        assert tape.pointer == i
        tape.move_right()

    assert tape.pointer == 7

    tape.move_right()
    assert tape.pointer == 0

    tape.move_left()
    assert tape.pointer == 7
    for i in range(7, 0, -1):
        assert tape.pointer == i
        tape.move_left()


def test_reset(tape: Tape) -> None:
    tape.move_right(3)
    assert tape.pointer == 3
    tape.reset()
    assert tape.pointer == 0


def test_bit(tape: Tape) -> None:
    assert tape.bit is False
    tape.toggle()
    assert tape.bit is True
    tape.toggle()
    assert tape.bit is False
