.SUFFIXES: .ui .py
rwildcard = $(wildcard $1$2)$(foreach d,$(wildcard $1*),$(call rwildcard,$d/,$2))
UI_FILES = $(call rwildcard,npc/gui/uis/,*.ui)
PY_FILES = $(UI_FILES:.ui=.py)

PREFIX = /usr/local

all: uis

.ui.py:
	pyuic5 $< -o $@

uis: $(PY_FILES)

.PHONY: test
test:
	python3 -m pytest

.PHONY: install
install:
	mkdir -p $(DESTDIR)$(PREFIX)/share/npc
	cp -R npc $(DESTDIR)$(PREFIX)/share/npc
	mkdir -p $(DESTDIR)$(PREFIX)/bin
	ln -s $(DESTDIR)$(PREFIX)/share/npc/npc.py $(DESTDIR)$(PREFIX)/bin/npc
	ln -s $(DESTDIR)$(PREFIX)/share/npc/npc-gui.py $(DESTDIR)$(PREFIX)/bin/npc-gui

.PHONY: uninstall
uninstall:
	rm -f $(DESTDIR)$(PREFIX)/bin/npc-gui
	rm -f $(DESTDIR)$(PREFIX)/bin/npc
	rm -rf $(DESTDIR)$(PREFIX)/share/npc
