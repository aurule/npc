from tests.fixtures import tmp_campaign

def test_gets_the_file(tmp_campaign):
    root = tmp_campaign.root

    assert tmp_campaign.plot_dir == root / "Plot"
