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

# Build Tag References

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

tag_table_template = jenv.get_template("tag_table.rst.j2")
tag_table_data = tag_table_template.render({
    "tags": sorted(ref_system.tags.values(), key=lambda s: s.name)
    })
tag_table_file = Path(f"docs/reference/tags/components/tag_table.rst")
with tag_table_file.open("w", newline="\n") as f:
    f.write(tag_table_data)

# Build Game System References

system_template = jenv.get_template("system.rst.j2")
systems_summary = []
for system_key in sorted(settings.get_system_keys()):
    system = settings.get_system(system_key)
    systems_summary.append(system)
    data = system_template.render({
        "header_characters": header_characters,
        "header_level": 0,
        "system": system,
        "len": len,
    })

    outfile = Path(f"docs/reference/systems/{system_key}.rst")
    with outfile.open("w", newline="\n") as f:
        f.write(data)

system_table_template = jenv.get_template("system_table.rst.j2")
system_table_data = system_table_template.render({
    "systems": systems_summary
    })
system_table_file = Path(f"docs/reference/systems/components/system_table.rst")
with system_table_file.open("w", newline="\n") as f:
    f.write(system_table_data)
