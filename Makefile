.SUFFIXES: .ui .py .qrc
rwildcard = $(wildcard $1$2)$(foreach d,$(wildcard $1*),$(call rwildcard,$d/,$2))

PREFIX := /usr/local

.PHONY: test
test:
	pytest --tb=no

.PHONY: coverage
coverage:
	pytest --cov=npc -q
	coverage html

.PHONY: install
install:
	mkdir -p $(DESTDIR)$(PREFIX)/share/npc
	cp -R npc $(DESTDIR)$(PREFIX)/share/npc
	mkdir -p $(DESTDIR)$(PREFIX)/bin
	ln -s $(DESTDIR)$(PREFIX)/share/npc/npc.py $(DESTDIR)$(PREFIX)/bin/npc

.PHONY: uninstall
uninstall:
	rm -f $(DESTDIR)$(PREFIX)/bin/npc
	rm -rf $(DESTDIR)$(PREFIX)/share/npc

.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d | xargs rm -fr
	find . -name '.cache' -type d | xargs rm -fr
	find . -name '<Temp*' -type d -print0 | xargs -0 rm -fr
	rm -fr deb_dist dist npc.egg-info .pytest_cache htmlcov .coverage

.PHONY: freeze
freeze:
	pip freeze | grep -v "pkg-resources" > requirements-dev.txt

.PHONY: deb
deb:
	python3 setup.py --command-packages=stdeb.command bdist_deb

h: help

.PHONY: help
help:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs

.PHONY: docs
docs:
	${MAKE} -C docs html
