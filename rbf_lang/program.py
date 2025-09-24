import warnings
from collections.abc import Sequence
from typing import Optional, Union, overload

from .command import Command
from .exceptions import InvalidProgramError, ProgramPointerError

_ProgramInitType = Union[str, Sequence[Command], "Program"]


class Program(Sequence[Command]):
    """RBF program."""

    _program: list[Command]
    _pointer: int
    _steps: int

    def __init__(
        self,
        program: _ProgramInitType,
        pointer: Optional[int] = None,
    ) -> None:
        if isinstance(program, Program):
            self._program = list(program.program)
            self._pointer = program.pointer
            self._steps = program.steps
            if pointer is not None:
                warnings.warn(
                    "Pointer argument is ignored when initializing Program with "
                    "another Program. Set it to None to disable this warning.",
                    stacklevel=2,
                )
        elif isinstance(program, (str, Sequence)):
            if isinstance(program, str):
                program = preprocess_program(program)
            validated_program = validate_program(program)
            self._program = validated_program
            pointer = 0 if pointer is None else pointer
            self._pointer = pointer
            self._steps = 0
        else:
            raise TypeError("Program must be initialized with a string or a sequence.")

    @property
    def program(self) -> Sequence[Command]:
        """Return a copy of the program commands."""
        return self._program.copy()

    @property
    def pointer(self) -> int:
        """Return the program pointer position -- 0-based index of the current command."""
        return self._pointer

    @property
    def steps(self) -> int:
        return self._steps

    def __len__(self) -> int:
        return len(self._program)

    @overload
    def __getitem__(self, index: int) -> Command: ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[Command]: ...

    def __getitem__(
        self,
        index_or_slice: Union[int, slice],
    ) -> Union[Command, Sequence[Command]]:
        if isinstance(index_or_slice, (int, slice)):
            return self._program[index_or_slice]
        else:
            raise TypeError("Index must be an int or a slice.")

    def _single_char_repr(self) -> str:
        return "".join(command.value for command in self._program)

    def __repr__(self) -> str:
        return f"Program({self._single_char_repr()!r})"

    def __str__(self) -> str:
        return self._single_char_repr()

    def _move_right_nostep(self) -> None:
        """Move the program pointer to the right without incrementing the step counter."""
        if self._pointer < len(self) - 1:
            self._pointer += 1
        else:
            raise ProgramPointerError("Program pointer overflow.")

    def move_right(self, N: int = 1) -> None:
        """Move the program pointer to the right."""
        for _ in range(N):
            self._steps += 1
            self._move_right_nostep()

    def _move_left_nostep(self) -> None:
        """Move the program pointer to the left without incrementing the step counter."""
        if self._pointer > 0:
            self._pointer -= 1
        else:
            raise ProgramPointerError("Program pointer underflow.")

    def move_left(self, N: int = 1) -> None:
        """Move the program pointer to the left."""
        for _ in range(N):
            self._steps += 1
            self._move_left_nostep()

    def loop_start(self, current_bit: bool) -> None:
        """If the current bit is zero, jump past matching ``)``. Else, continue (loop)."""
        if self.command != Command.LOOP_START:
            raise ValueError("Not at a loop start.")

        # NOTE: we want to increment even if we end up raising an error.
        self._steps += 1

        if not current_bit:
            try:
                # The current bit is zero, so we jump past the matching ).
                bracket_depth = 1
                while bracket_depth > 0:
                    self._move_right_nostep()
                    if self.command == Command.LOOP_START:
                        bracket_depth += 1
                    elif self.command == Command.LOOP_END:
                        bracket_depth -= 1

            except ProgramPointerError:
                # We've hit the end of the program without finding the matching ).
                raise InvalidProgramError("Unmatched loop start.") from None

        # We are now at the matching ), but we need to move past it, so move right once more.
        try:
            self._move_right_nostep()
        except ProgramPointerError:
            # We cannot move past the matching ) because we are at the end of the program.
            # Just let the program end by re-raising the ProgramPointerError.
            raise

    def loop_end(self, current_bit: bool) -> None:
        """If the current bit is zero, jump back to just after matching ``(``. Else, continue."""
        if self.command != Command.LOOP_END:
            raise ValueError("Not at a loop end.")

        self._steps += 1

        if not current_bit:
            try:
                # The current bit is zero, so we jump back to just after the matching (.
                bracket_depth = 1
                while bracket_depth > 0:
                    self._move_left_nostep()
                    if self._program[self._pointer] == Command.LOOP_START:
                        bracket_depth -= 1
                    elif self._program[self._pointer] == Command.LOOP_END:
                        bracket_depth += 1

            except ProgramPointerError:
                raise InvalidProgramError("Unmatched loop end.") from None

        # We are now at the matching (, but we need to move just after it, so move right once.
        # NOTE: We don't need to worry about hitting the end of the program here.
        self._move_right_nostep()

    def reset(self) -> None:
        """Reset the program pointer and step counter."""
        self._pointer = 0
        self._steps = 0

    @property
    def command(self) -> Command:
        """Return the current command. Raises :class:`rbf_lang.exceptions.ProgramPointerError`
        if the program is empty."""
        if len(self) == 0:
            raise ProgramPointerError("Program is empty.")
        return self._program[self._pointer]

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Program):
            return self._program == other.program
        elif isinstance(other, str):
            return str(self) == other
        else:
            return False

    def __hash__(self) -> int:
        return hash(str(self))

    def copy(self) -> "Program":
        """Return a copy of the program."""
        return Program(self)


def preprocess_program(program: str) -> str:
    """Preprocess the RBF program by removing comments and spaces. For example:

    >>> program = \"\"\"
    ... # x=?, y=0, f=0
    ... (>>*<<)        # set f if x is set
    ... >>(            # if f is set
    ...     <(>*<)*    # set y
    ...     <*(>>*<<)  # unset x
    ... >>)
    ... <(>*<)         # if y is set, unset f
    ... \"\"\"
    >>> preprocess_program(program)
    '(>>*<<)>>(<(>*<)*<*(>>*<<)>>)<(>*<)'
    """

    # Split into lines
    lines = program.split("\n")
    # For each line, remove any characters after a # (comments)
    lines = [line.split("#", 1)[0] for line in lines]
    # Join the lines back together
    program = "".join(lines)
    # Remove spaces
    program = program.replace(" ", "")

    return program

    # ValueError: Invalid RBF command: '+'


def validate_program(program: Union[str, Sequence[Command]]) -> list[Command]:
    """Check all commands are valid and that brackets are balanced. Return a list of Commands.

    >>> validate_program("()")
    [<Command.LOOP_START: '('>, <Command.LOOP_END: ')'>]
    >>> validate_program("+")
    Traceback (most recent call last):
        ...
    rbf_lang.exceptions.InvalidProgramError: '+' is not a valid Command
    """

    parsed_commands: Sequence[Command]
    if isinstance(program, str):
        # Remove any characters that are not RBF commands.
        # Convert the string to a list of Commands.
        try:
            parsed_commands = [Command(command) for command in program]
        except ValueError as e:
            raise InvalidProgramError(str(e)) from None
    else:
        # The program is already a list of Commands.
        parsed_commands = list(program)

    bracket_depth = 0  # Keep track of the depth of the brackets.
    for command in parsed_commands:
        if command == Command.LOOP_START:
            bracket_depth += 1
        elif command == Command.LOOP_END:
            bracket_depth -= 1

        if bracket_depth < 0:
            raise InvalidProgramError("Unmatched loop end.")

    if bracket_depth != 0:
        raise InvalidProgramError("Unmatched loop start.")

    return parsed_commands
