"""
Reversible BitFuck (RBF) interpreter
"""

__version__ = "0.2.2"
__author__ = "Marcin Konowalczyk"
__license__ = "MIT"

from . import program, reverse, runner, tape

Program = program.Program
Tape = tape.Tape
run = runner.run
reverse_program = reverse.reverse_program

__all__ = ["Program", "Tape", "reverse_program", "run"]
