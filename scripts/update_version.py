import click
import re
import os
from pathlib import Path

def handle_placeholder(
    root_dir: Path,
    version: str,
    excludes: list[str] = None,
    ):
    excludes = excludes or []

    for root, dirs, files in os.walk(root_dir):
        root = Path(root)

        for name in files:
            file_path = root / name
            if any([file_path.match(pattern) for pattern in excludes]):
                continue

            try:
                old_contents = file_path.read_text()
            except:
                continue
            new_contents = re.sub(r"NEW_VERSION", version, old_contents)
            if new_contents != old_contents:
                file_path.write_text(new_contents)

@click.command
@click.option(
    "-v", "--version",
    "version",
    required=True,
    type=str,
    )
def update_version(version):
    # handle version file
    version_file = Path("src/npc/__init__.py")
    old_contents = version_file.read_text()
    new_contents = re.sub(r"version__\s+=\s+\"(.*)\"", f"version__ = \"{version}\"", old_contents)
    version_file.write_text(new_contents)

    # handle docs
    docs_root = Path("docs")

    docs_conf = docs_root / "conf.py"
    old_contents = docs_conf.read_text()
    new_contents = re.sub(r"release\s+=\s+\"(.*)\"", f"release = \"{version}\"", old_contents)
    docs_conf.write_text(new_contents)

    handle_placeholder(docs_root, version, [])

    # handle defs
    handle_placeholder(
        Path("src/npc/settings/systems"),
        version,
        ["*.py"])
    handle_placeholder(
        Path("src/npc/settings/types"),
        version,
        ["*.py"])

if __name__ == '__main__':
    update_version()
