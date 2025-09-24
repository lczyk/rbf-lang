import warnings
from collections.abc import Sequence
from typing import Optional, Union, overload

_TAPE_SIZE = 8

_TapeInitType = Union[int, str, Sequence, "Tape"]


class Tape(Sequence[bool]):
    """Tape is a circular tape of 1-bit cells. The tape is initialized to all 0s."""

    _tape: list[bool]
    _pointer: int

    def __init__(
        self,
        tape: _TapeInitType = _TAPE_SIZE,
        pointer: Optional[int] = None,
    ) -> None:
        if isinstance(tape, int):
            # Initialize the tape with all 0s
            self._tape = [False] * tape
        elif isinstance(tape, str):
            # Initialize the tape with the given string
            self._tape = [bool(int(x)) for x in tape]
        elif isinstance(tape, Tape):
            # Copy the tape
            self._tape = tape._tape.copy()
            if pointer is not None:
                warnings.warn(
                    "Pointer argument is ignored when initializing Tape with "
                    "another Tape. Set it to None to disable this warning.",
                    stacklevel=2,
                )
            pointer = tape._pointer
        elif isinstance(tape, Sequence):
            # Initialize the tape with the given sequence
            self._tape = [bool(x) for x in tape]
        else:
            raise TypeError("Tape must be initialized with an int or a sequence.")

        self._pointer = 0 if pointer is None else pointer

    def __len__(self) -> int:
        return len(self._tape)

    @property
    def tape(self) -> Sequence[bool]:
        # Return a copy of the tape
        return list(self._tape)

    @property
    def pointer(self) -> int:
        return self._pointer

    @overload
    def __getitem__(self, index: int) -> bool: ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[bool]: ...

    def __getitem__(self, index_or_slice: Union[int, slice]) -> Union[bool, Sequence[bool]]:
        if isinstance(index_or_slice, (int, slice)):
            return self._tape[index_or_slice]
        else:
            raise TypeError("Index must be an int or a slice.")

    def toggle(self) -> None:
        """Toggle the current cell."""
        self._tape[self._pointer] = not self._tape[self._pointer]

    def move_right(self, N: int = 1) -> None:
        """Move the tape head to the right."""
        self._pointer = (self._pointer + N) % len(self)

    def move_left(self, N: int = 1) -> None:
        """Move the tape head to the left."""
        self._pointer = (self._pointer - N) % len(self)

    def _single_char_repr(self) -> str:
        return "".join("1" if bit else "0" for bit in self._tape)

    def __repr__(self) -> str:
        return f"Tape({self._single_char_repr()!r})"

    def __str__(self) -> str:
        return self._single_char_repr()

    def reset(self) -> None:
        """Reset the tape to all 0s and move the head to the first cell."""
        self._tape = [False] * len(self)
        self._pointer = 0

    @property
    def bit(self) -> bool:
        return self._tape[self._pointer]

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Tape):
            return self._tape == other._tape
        elif isinstance(other, str):
            return str(self) == other
        elif isinstance(other, Sequence):
            return self._tape == [bool(x) for x in other]
        else:
            return False

    def __hash__(self) -> int:
        return hash(str(self))

    def copy(self) -> "Tape":
        """Return a copy of the tape."""
        return Tape(self)
