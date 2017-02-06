.SUFFIXES: .ui .py
rwildcard = $(wildcard $1$2)$(foreach d,$(wildcard $1*),$(call rwildcard,$d/,$2))
UI_FILES = $(call rwildcard,npc/gui/uis/,*.ui)
PY_FILES = $(UI_FILES:.ui=.py)

.ui.py:
	pyuic5 $< -o $@

uis: $(PY_FILES)

.PHONY: test
test:
	python3 -m pytest
