import npc
import pytest

def test_listing_formatter():
    formatter = npc.formatters.get_listing_formatter('markdown')
    assert formatter == npc.formatters.markdown.listing
    formatter = npc.formatters.get_listing_formatter('html')
    assert formatter == npc.formatters.html.listing
    formatter = npc.formatters.get_listing_formatter('json')
    assert formatter == npc.formatters.json.listing

def test_report_formatter():
    formatter = npc.formatters.get_report_formatter('markdown')
    assert formatter == npc.formatters.markdown.report
    formatter = npc.formatters.get_report_formatter('html')
    assert formatter == npc.formatters.html.report
    formatter = npc.formatters.get_report_formatter('json')
    assert formatter == npc.formatters.json.report
