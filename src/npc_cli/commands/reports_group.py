import click
from click import echo, BadParameter

from npc import characters
from npc.reporters import tag_reporter
from npc_cli.presenters import tabularize
from npc_cli.helpers import campaign_or_fail
from npc_cli.errors import CampaignNotFoundException

from .main_group import cli, pass_settings

##########################
# Config reports group
##########################

@cli.group()
def report():
    """Show stats about the characters in this campaign"""

#######################
# Show tag stastistics
#######################

@report.command()
@click.option("-t", "--tag", "tag_name",
    help="Tag to analyze")
@click.option("-c", "--context",
    help="Parent context if tag is a subtag. Use '*' to disregard parent.")
@pass_settings
def values(settings, tag_name, context):
    """Show a how many times each unique value appears for the given tag

    This command only works within an existing campaign

    The '--context' option is only needed if '--tag' is a subtag like role.
    """
    campaign = campaign_or_fail(settings)

    campaign.characters.seed()

    spec = campaign.get_tag(tag_name)
    if spec.needs_context and context != "*":
        valid_contexts = list(spec.contexts.keys()) + ["*"]
        if (not context) or (context not in valid_contexts):
            raise click.BadParameter(f"{tag_name} tag requires context to be one of {valid_contexts}", param_hint=['-c', '--context'])
        data = tag_reporter.subtag_value_counts_report(tag_name, context)
        prefix: str = f"@{tag_name} ({context})"
    else:
        data = tag_reporter.value_counts_report(tag_name)
        prefix: str = f"@{tag_name} tag"

    title: str = f"{prefix} values report"
    headers = ("Value", "Count")
    echo(tabularize(data, headers=headers, title=title))
