#!/usr/bin/env python3.5

"""
Executable entry point for the NPC GUI interface.
"""

import sys
import npc

if __name__ == '__main__':
    npc.gui.start(sys.argv[1:])
