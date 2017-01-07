.SUFFIXES: .ui .py
UI_FILES=$(wildcard npc/gui/uis/*.ui)
PY_FILES=$(UI_FILES:.ui=.py)

.ui.py:
	pyuic5 $< -o $@

uis: $(PY_FILES)

test:
	python -m pytest
