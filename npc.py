#!/usr/bin/env python3.5

"""
Executable entry point for the NPC CLI interface.
"""

import sys
import npc

if __name__ == '__main__':
    npc.cli(sys.argv[1:])
