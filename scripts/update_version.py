import click
import re
import os
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

    docs_root = Path("docs")

    docs_conf = docs_root / "conf.py"
    old_contents = docs_conf.read_text()
    new_contents = re.sub(r"release\s+=\s+\"(.*)\"", f"release = \"{version}\"", old_contents)
    docs_conf.write_text(new_contents)

    doc_excludes = ["_build", "source"]
    for root, dirs, files in os.walk(docs_root):
        dirs = filter(lambda d: d not in doc_excludes, dirs)
        root = Path(root)

        for name in files:
            file_path = root / name
            try:
                old_contents = file_path.read_text()
            except:
                continue
            new_contents = re.sub(r"NEW_VERSION", version, old_contents)
            if new_contents != old_contents:
                file_path.write_text(new_contents)

if __name__ == '__main__':
    update_version()
