import click
from pathlib import Path

headers = {
    "added": "Added",
    "changed": "Changed",
    "removed": "Removed",
    "fixed": "Fixed",
}

@click.command()
@click.option(
    "-v", "--version",
    "version",
    required=True,
    type=str,
    prompt="What version is this changelog for?"
    )
@click.option(
    "--live/--dry-run",
    type=bool,
    default=True,
    )
def build_changelog(version, live):
    changes_root = Path("changes/")
    buckets = {
        "added": [],
        "changed": [],
        "removed": [],
        "fixed": [],
    }
    for change_file in changes_root.glob("[!.]*"):
        summary = change_file.read_text()
        bucket_name = change_file.suffix[1:]
        buckets[bucket_name].append(summary)
        if live:
            change_file.unlink()

    changelog_file = Path("changelog") / f"{version}.md"
    with changelog_file.open("w", newline="\n") as f:
        f.write(f"# Changelog for NPC {version}\n")

        for bucket_name, change_lines in buckets.items():
            if not change_lines:
                continue
            f.write(f"\n## {headers[bucket_name]}\n")
            f.write("\n* ")
            f.write("* ".join(change_lines))

    latest_changelog = Path("CHANGELOG.md")
    current_contents = changelog_file.read_text()
    with latest_changelog.open("w", newline="\n") as f:
        f.write(current_contents)
        f.write("For changes in previous versions, see the files in `changelog/`.")

if __name__ == '__main__':
    build_changelog()
