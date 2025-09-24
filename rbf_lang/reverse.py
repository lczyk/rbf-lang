import logging
from collections.abc import Sequence
from functools import singledispatch
from typing import Union, overload

from .command import Command
from .program import Program

logger = logging.getLogger("rbf")

_COMMAND_TRANSLATION = {
    Command.TOGGLE: Command.TOGGLE,
    Command.TAPE_RIGHT: Command.TAPE_LEFT,
    Command.TAPE_LEFT: Command.TAPE_RIGHT,
    Command.LOOP_START: Command.LOOP_END,
    Command.LOOP_END: Command.LOOP_START,
}

_STRING_TRANSLATION = {k.value: v.value for k, v in _COMMAND_TRANSLATION.items()}


# mypy x singledispatch
# https://github.com/python/mypy/issues/8356#issuecomment-884548381


@singledispatch
def _reverse_program(
    program: Union[str, Sequence[Command], Program],
) -> Union[str, Sequence[Command], Program]:
    """Reverse the RBF program."""
    raise TypeError(f"Cannot reverse program of type {type(program)}")


@_reverse_program.register
def _(program: list) -> list:
    return [_COMMAND_TRANSLATION[command] for command in reversed(program)]


@_reverse_program.register
def _(program: str) -> str:
    _program = Program(program)
    return str(reverse_program(_program))


@_reverse_program.register
def _(program: Program) -> Program:
    _program = _reverse_program(program.program)
    return Program(_program)
    # return Program(reverse_program(program.program))


@overload
def reverse_program(program: Program) -> Program: ...


@overload
def reverse_program(program: Sequence[Command]) -> Sequence[Command]: ...


@overload
def reverse_program(program: str) -> str: ...


def reverse_program(
    program: Union[str, Sequence[Command], Program],
) -> Union[str, Sequence[Command], Program]:
    return _reverse_program(program)
