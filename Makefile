.SUFFIXES: .ui .py .qrc
rwildcard = $(wildcard $1$2)$(foreach d,$(wildcard $1*),$(call rwildcard,$d/,$2))
UI_FILES := $(call rwildcard,npc/gui/uis/,*.ui)
COMPILED_UI_FILES := $(UI_FILES:.ui=.py)
RESOURCE_FILES := $(call rwildcard,npc/gui/uis/,*.qrc)
COMPILED_RESOURCE_FILES := $(RESOURCE_FILES:%.qrc=%_rc.py)
IMAGES := $(call rwildcard,npc/gui/uis/icons,*.svg)

PREFIX := /usr/local

all: resources uis

.ui.py:
	pyuic5 $< | sed 's/import \(.*_rc\)/from . import \1/g' > $@

%_rc.py : %.qrc $(IMAGES)
	pyrcc5 $< -o $@

uis: $(COMPILED_UI_FILES)

resources: $(COMPILED_RESOURCE_FILES)

.PHONY: test
test:
	python3 -m pytest

.PHONY: coverage
coverage:
	python3 -m pytest --cov=npc -q
	coverage html

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

.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d | xargs rm -fr
	find . -name '.cache' -type d | xargs rm -fr
	find . -name '<Temp*' -type d -print0 | xargs -0 rm -fr
	rm -fr deb_dist dist npc.egg-info .pytest_cache htmlcov .coverage

.PHONY: clean-all
clean-all: clean
	rm -fr $(COMPILED_UI_FILES) $(COMPILED_RESOURCE_FILES)

.PHONY: freeze
freeze:
	pip freeze | grep -v "pkg-resources" > requirements-dev.txt

.PHONY: deb
deb:
	python3 setup.py --command-packages=stdeb.command bdist_deb

.PHONY: help
help:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs
