import click
import os
from pathlib import Path

@click.command
@click.option(
    "--live/--dry-run",
    type=bool,
    default=True,
    )
def clean(live):
    def rmdir_or_print(p: Path):
        if not p.exists():
            return
        if live:
            # rmdir
            for root, dirs, files in os.walk(p, topdown=False):
                root = Path(root)
                for name in files:
                    (root / name).unlink()
                for name in dirs:
                    (root / name).rmdir()
            p.rmdir()
        else:
            print(p)

    package_root = Path(".")
    for p in package_root.glob("**/__pycache__/"):
        rmdir_or_print(p)

    rmdir_or_print(package_root / ".pytest_cache")
    rmdir_or_print(package_root / "build")
    rmdir_or_print(package_root / "dist")

if __name__ == '__main__':
    clean()
