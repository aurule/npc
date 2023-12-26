# Release Guide

The tag format is `vX.Y.Z`

To make a release:

1. run `poe release --version X.Y.Z`
    * This creates the branch `release/vX.Y.Z`
    * Generates the new changelog file
    * Updates the version in `npc/__init__.py`
2. Review the created `CHANGELOG.md` and `changelog/vX.Y.Z.md` files
3. Commit
4. Merge into `master` branch
5. Create a tag `vX.Y.Z`
6. Push `master`
7. Delete release branch
8. Merge `master` back into `develop`
