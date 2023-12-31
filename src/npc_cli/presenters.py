from click import wrap_text
from typing import Generator

from npc.campaign import Campaign

def directory_list(dirs: list) -> str:
    """Format a list of directory names

    Args:
        dirs (list): List of Paths to one or more directories

    Returns:
        str: Description of the given Paths
    """
    return "\n".join([f"  {dirname}/" for dirname in dirs])

def type_list(types: dict) -> str:
    """Format a dict of type defs

    Args:
        types (dict): Dict of type definitions to format

    Returns:
        str: List of type keys joined by commas
    """
    return ", ".join([f"'{t}'" for t in types.keys()])

def campaign_info(campaign: Campaign) -> str:
    """Show information about a campaign

    Shows some brief info and stats

    Args:
        campaign (Campaign): Campaign to describe

    Returns:
        str: Info about the campaign
    """
    infos = [
        f"{'---Campaign Info---':>22}",
        f"{'Name:':>12} {campaign.name}",
        f"{'Description:':>12} {campaign.desc}",
        f"{'System:':>12} {campaign.system.name}",
        f"{'Plot Files:':>12} {campaign.latest_plot_index}",
        f"{'Sessions:':>12} {campaign.latest_session_index}",
    ]
    return "\n".join(infos)

def tabularize(data: list[tuple], headers: tuple[str], title: str = None) -> str:
    """Generate a multimarkdown-style table

    Creates a table with the given data, headers, and optional title. Tables look like:

                                [Character Types for New World of Darkness]
    | Name       | Key        | Description                                                           |
    |------------|------------|-----------------------------------------------------------------------|
    | Werewolf   | werewolf   | Shapechanging warriors who guard the spirit world                     |
    | Spirit     | spirit     | A disembodied representation of a thing, place, or concept            |
    | Vampire    | vampire    | A cursed denizen of the night who feeds on blood.                     |
    | Mage       | mage       | An awakened human with access to world-shaping magic.                 |
    | Changeling | changeling | A human who was captured by the fae and returned to the mundane world |

    Args:
        data (list[tuple]): List of row data. Each row is a tuple whose contents are the values of each column.
        headers (tuple[str]): List of header strings.
        title (str): Title to add to the table (default: `None`)

    Returns:
        str: Formatted table of data
    """
    rows = [headers, *data]
    colwidths: list = []
    for index in range(len(headers)):
        colwidths.append(max([len(str(row[index])) for row in rows]))

    lines: list[str] = [
        "| " + " | ".join([f"{rows[0][colnum]:<{width}}" for colnum, width in enumerate(colwidths)]) + " |",
        "|" + "|".join(["-"*(width+2) for width in colwidths]) + "|"
    ]

    if title:
        title = f"[{title}]"
        title_offset: float = (len(title) + len(lines[0]))/2
        lines.insert(0, f"{title:>{title_offset:.0f}}")

    for row in rows[1::]:
        lines.append("| " + " | ".join([f"{row[colnum]:<{width}}" for colnum, width in enumerate(colwidths)]) + " |")

    return "\n".join(lines)

def wrapped_paragraphs(bigstring: str) -> Generator[str, None, None]:
    """Turn a large string into multiple word-wrapped strings

    This treats each line in bigstring as a single paragraph and does word wrapping using Click's wrap_text
    function.

    Args:
        bigstring (str): The string to break into paragraphs and wrap

    Yields:
        One word-wrapped string per line in bigstring.
    """
    for line in bigstring.splitlines():
        yield wrap_text(line)

def tag_table_data(tags: dict) -> Generator[tuple, None, None]:
    """Generate tag and subtag table lines

    Args:
        tags (dict): Dict of tag specs to show

    Yields:
        tuple of tag info
    """
    for tag in tags.values():
        if tag.needs_context:
            continue
        yield [tag.name, tag.desc]
        for subtag_name in tag.subtags:
            subtag = tags.get(subtag_name).in_context(tag.name)
            yield [f"\u2514 {subtag.name}", subtag.desc]
