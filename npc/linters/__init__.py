"""
Linters for verifying the correctness of certain character types

The `commands.lint` function can lint all basic files, but special character
types sometimes need extra checks. The linters in this package encapsulate that
logic.

All linter packages have a single main entry point `lint` which accepts a
character information dict. Various keyword arguments are used for options and
supporting data.
"""

from . import changeling
