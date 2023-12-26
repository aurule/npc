# All migration classes must be imported before they will be detected by our
# migrations property.
from .migration_1to2 import Migration1to2

# Last, we import the migrator itself
from .settings_migrator_class import SettingsMigrator

__all__ = ["SettingsMigrator"]
