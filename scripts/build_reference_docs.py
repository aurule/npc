from npc.settings import Settings
import yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

header_characters = ["#", "=", "-", "~", "^"]

# build global tags references

settings = Settings()
ref_system = settings.get_system("generic")

jenv = Environment(
    loader = FileSystemLoader("docs/reference/templates/"),
    auto_reload = False,
    autoescape = False,
)
tag_template = jenv.get_template("tag.rst.j2")

for tag in ref_system.tags.values():
    if tag.needs_context:
        continue

    data = tag_template.render({
        "header_characters": header_characters,
        "header_level": 0,
        "tag": tag,
        "parents": [],
        "len": len,
        "all_tags": ref_system.tags
        })

    outfile = Path(f"docs/reference/tags/{tag.name}.rst")
    with outfile.open("w", newline="\n") as f:
        f.write(data)

# build systems references
