from npc.cli import progress_bar
import pytest

def test_bar_creates_correct_ratio(capsys):
    progress_bar.bar(50, 100)

    _, err = capsys.readouterr()

    assert '|##################################################--------------------------------------------------| 50.0%' in err

def test_bar_at_100_includes_newline(capsys):
    progress_bar.bar(5, 5)

    _, err = capsys.readouterr()

    assert '100.0% \r\n' in err
