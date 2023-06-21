from jinja2 import BaseLoader, FileSystemLoader, TemplateNotFound
from pathlib import Path
# from importlib import resources

from npc.campaign import Campaign

import logging
logger = logging.getLogger(__name__)

class FallbackLoader(BaseLoader):
    """Jinja template loader that attempts to return a fallback template if the requested template is not found

    FallbackLoader uses the passed loader to search for templates as usual. If a template is not found, it
    constructs a fallback template using the original template's suffix and the static string
    self.fallback_stem for the name. If the fallback also cannot be found, FallbackLoader will fail as normal.
    """
    def __init__(self, loader: BaseLoader):
        self.loader: BaseLoader = loader
        self.fallback_stem: str = "default"

    def get_source(self, environment, template: str) -> str:
        """Get a template

        Get the named template using our loader. If that isn't found, this then tries to get the fallback
        template instead. If that also fails, a TemplateNotFound is raised.

        Args:
            environment (Environment): Jinja env for template compilation
            template (str): Template to find

        Returns:
            str: Template path

        Raises:
            TemplateNotFound: Raised if both the template and fallback are not found
        """
        try:
            return self.loader.get_source(environment, template)
        except TemplateNotFound:
            fallback = self.fallback(template)
            logger.info(f"No template for {template}, falling back on {fallback}")
            return self.loader.get_source(environment, fallback)

    def fallback(self, template: str) -> str:
        """Get the fallback template name

        Replaces the template name with our fallback string, leaving the suffix and path components in place.

        Args:
            template (str): Template we need the fallback for

        Returns:
            str: Fallback template name
        """
        template_path = Path(template)
        return str(template_path.with_stem(self.fallback_stem))

class CharacterFallbackLoader(FallbackLoader):
    """Jinja template loader for character templates

    CharacterFallbackLoader searches the following directories in order for the requested template:
    * <campaign>/.npc/templates/characters
    * <user settings>/templates/characters/<campaign system>
    * <npc package>/templates/characters/<campaign system>
    * <user settings>/templates/characters
    * <npc package>/templates/characters

    This sets the order of precedence to campaign, user (system-specific), global (system-specific),
    user (generic), global (generic). If the named template isn't found, it falls back on "character.<suffix>".

    Typical use would be searching for something like "changeling.html" with a campaign system of "nwod". The
    search sequence would look like:
    1. <campaign>/.npc/templates/characters/changeling.html
    2. <user settings>/templates/characters/<campaign system>/changeling.html
    3. <npc package>/templates/characters/<campaign system>/changeling.html
    4. <user settings>/templates/characters/changeling.html
    5. <npc package>/templates/characters/changeling.html
    And if that isn't found:
    6. <campaign>/.npc/templates/characters/character.html
    7. <user settings>/templates/characters/<campaign system>/character.html
    8. <npc package>/templates/characters/<campaign system>/character.html
    9. <user settings>/templates/characters/character.html
    10. <npc package>/templates/characters/character.html

    Since in the worst case this results in 10 file lookups for every template request, it's a good idea to
    set up the environment with auto_reload=False and call env.cache.clear() as needed.
    """
    def __init__(self, campaign: Campaign):
        personal_templates = campaign.settings.personal_dir / "templates" / "characters"
        internal_templates = campaign.settings.install_base / "templates" / "characters"
        self.loader = FileSystemLoader([
            campaign.settings_dir / "templates" / "characters",
            personal_templates / campaign.system_key,
            internal_templates / campaign.system_key,
            personal_templates,
            internal_templates,
        ])
        self.fallback_stem = "character"
        self.system_key = campaign.system_key
