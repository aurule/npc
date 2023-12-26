import click
import re
from pathlib import Path

@click.command
@click.option(
    "-v", "--version",
    "version",
    required=True,
    type=str,
    )
def update_version(version):
    version_file = Path("src/npc/__init__.py")
    old_contents = version_file.read_text()
    new_contents = re.sub(r"version__\s+=\s+\"(.*)\"", f"version__ = \"{version}\"", old_contents)
    version_file.write_text(new_contents)

    docs_file = Path("docs/conf.py")
    old_contents = docs_file.read_text()
    new_contents = re.sub(r"release\s+=\s+\"(.*)\"", f"release = \"{version}\"", old_contents)
    docs_file.write_text(new_contents)

if __name__ == '__main__':
    update_version()
