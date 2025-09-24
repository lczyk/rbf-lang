from typing import Callable, Optional

from .command import Command
from .program import Program, ProgramPointerError, _ProgramInitType
from .tape import Tape, _TapeInitType


def run(
    program: _ProgramInitType,
    tape: _TapeInitType,
    max_steps: int = 1000,
    callback: Optional[Callable[[Program, Tape], bool]] = None,
) -> tuple[Program, Tape]:
    """Run the RBF program. The program will run until it reaches
    the maximum number of steps or the callback returns True."""

    program = Program(program)
    tape = Tape(tape)
    try:
        while program.steps < max_steps:
            # Run the callback and break if it returns True
            if callback and callback(program, tape):
                break

            command = program.command
            bit = tape.bit

            if command == Command.TOGGLE:
                tape.toggle()
                program.move_right()
            elif command == Command.TAPE_RIGHT:
                tape.move_right()
                program.move_right()
            elif command == Command.TAPE_LEFT:
                tape.move_left()
                program.move_right()
            elif command == Command.LOOP_START:
                program.loop_start(bit)
            elif command == Command.LOOP_END:
                program.loop_end(bit)
            else:
                raise ValueError(f"Unknown command: {command}")

    except ProgramPointerError:
        # We've moved off the end of the program. This is fine.
        pass

    return program, tape
