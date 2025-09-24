from rbf_lang import Program, Tape, run


def test_run_toggle() -> None:
    source = "*>" * 8
    tape_size = 8

    program, tape = run(
        source,
        tape_size,
    )

    assert program == source
    assert tape == "11111111"

    source = "*<" * 8
    program, tape = run(
        source,
        tape,
    )

    assert program == source
    assert tape == "00000000"


def test_run_callback() -> None:
    source = "*>" * 8
    tape_size = 8

    def callback(program: Program, tape: Tape) -> bool:
        return program.steps == 5

    program, tape = run(
        source,
        tape_size,
        callback=callback,
    )

    assert program.steps == 5
    assert tape == "11100000"


def test_run_max_steps() -> None:
    source = "*>" * 8
    tape_size = 8

    program, tape = run(
        source,
        tape_size,
        max_steps=5,
    )

    assert program.steps == 5
    assert tape == "11100000"


def test_run_loop_behavior() -> None:
    source = "()"
    program, tape = run(source, 8, max_steps=10)

    assert program.steps == 1
    assert tape == "00000000"

    source = "*(>)"
    program, tape = run(source, 8, max_steps=10)
    assert program.steps == 10
