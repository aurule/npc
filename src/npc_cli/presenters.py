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
        f"{'System:':>12} {campaign.system_key}",
        f"{'Plot Files:':>12} {campaign.latest_plot_index}",
        f"{'Sessions:':>12} {campaign.latest_session_index}",
    ]
    return "\n".join(infos)

def tabularize(rows: list[list], headers: list[str], title: str = None) -> str:
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
        rows (list[list]): List of row data. Each row is a list whose contents are the values of each column.
        headers (list[str]): List of header strings.
        title (str): Title to add to the table (default: `None`)

    Returns:
        str: Formatted table of data
    """
    rows.insert(0, headers)
    colwidths: list = []
    for index in range(len(headers)):
        colwidths.append(max([len(row[index]) for row in rows]))

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
