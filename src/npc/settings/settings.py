"""
Load and save settings info
"""

from pathlib import Path

# file loading
# * each successive file merges or overwrites keys with the same path
#     - lists are merged
#     - dicts are merged
#     - other values are overwritten
# * location search order
#     - internal
#     - user home
#     - campaign (discovered on invocation)
# * file load order
#     - `settings.yaml`
#     - campaign.system
# * special handling
#     - systems can `inherit` from another system. Before merging the target system, check its `inherits` property and load that system first. Then finish merging the target system.
# * lazy load `system/type/*.yaml` individually or singly as required
