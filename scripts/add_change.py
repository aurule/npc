import click
from pathlib import Path

change_types = {
    "Addition": "added",
    "Change": "changed",
    "Removal": "removed",
    "Fix": "fixed"
}

@click.command()
@click.option(
    "-t", "--type",
    "change_type",
    type=click.Choice(change_types.keys()),
    prompt="What type of change is this?",
    required=True,
    )
@click.option(
    "-m", "--message",
    type=str,
    prompt="One-line summary of the change",
    required=True,
    )
@click.option(
    "-l", "--label",
    type=str,
    prompt="Shorthand reference to jog your memory",
    required=True,
    )
def add_change(change_type, message, label):
    suffix = change_types[change_type]
    target = Path("changes") / f"{label}.{suffix}"
    with target.open('w', newline="\n") as f:
        f.write(message)

if __name__ == '__main__':
    add_change()
