import npc
import pytest

# tests to do
# json loading ignores comments
# error prints arbitrary message to stderr
# flatten(['some text', 5, ['yet more']]) should yield ['some text', 5, 'yet more']
# find campaign root returns folder containing .npc or current directory if not found
# new class using Singleton yields the same object when created again:
