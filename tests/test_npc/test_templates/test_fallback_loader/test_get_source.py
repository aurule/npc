from jinja2 import FileSystemLoader

from npc.templates import FallbackLoader

def test_gets_named_template_if_exists(tmp_path):
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    named = templates_dir / "named.html"
    named.touch()
    loader = FallbackLoader(FileSystemLoader(templates_dir))

    result = loader.get_source(None, "named.html")

    assert result[1] == str(named)

def test_gets_fallback_template_if_named_not_found(tmp_path):
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    fallback = templates_dir / "default.html"
    fallback.touch()
    loader = FallbackLoader(FileSystemLoader(templates_dir))

    result = loader.get_source(None, "named.html")

    assert result[1] == str(fallback)
