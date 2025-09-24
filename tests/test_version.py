from pathlib import Path

from conftest import __project_root__
from packaging.version import Version

PYPROJECT_FILE = __project_root__ / "pyproject.toml"


def get_version_from_snapcraft(file: Path) -> Version:
    # Ideally we would parse the toml, but python backporting support for
    # tomli or other toml parsers is a but meh, so we will just read the file
    lines = file.read_text().splitlines()
    for line in lines:
        if line.startswith("version:"):
            version_str = line.split(":", 1)[1].split("#", 1)[0].strip().strip('"').strip("'")
            return Version(version_str)
    raise ValueError(f"Version not found in {file}")


def test_version_in_snapcraft_matches_version_in_init() -> None:
    from rbf_lang import __version__

    snapcraft_file = __project_root__ / "snap" / "snapcraft.yaml"
    snapcraft_version = get_version_from_snapcraft(snapcraft_file)
    init_version = Version(__version__)
    assert snapcraft_version == init_version, (
        f"Version mismatch: {snapcraft_version} in 'snapcraft.yaml' "
        f"and {init_version} in '__init__.py'. If in doubt, "
        "__version__ in '__init__.py' is the source of truth."
    )
