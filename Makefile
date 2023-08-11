.SUFFIXES: .ui .py .qrc
rwildcard = $(wildcard $1$2)$(foreach d,$(wildcard $1*),$(call rwildcard,$d/,$2))

PREFIX := /usr/local

.PHONY: test coverage unused
test:
	pytest --tb=no
coverage:
	pytest --cov=npc --cov=npc_cli --cov-report=html --cov-report=term -q -p no:pretty
unused:
	vulture src/npc tests

requirements = requirements.txt requirements-ci.txt requirements-dev.txt docs/requirements.txt
$(requirements): %.txt: %.in
	pip-compile $< --resolver=backtracking --quiet

requirements: $(requirements)

.PHONY: clean
clean:
	-find . -name '__pycache__' -type d | xargs rm -fr
	-rm -fr .pytest_cache htmlcov .coverage build dist
	${MAKE} -C docs clean

.PHONY: help
h: help
help:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs

.PHONY: docs
docs:
	${MAKE} -C docs html

.PHONY: livedocs
livedocs:
	sphinx-autobuild docs docs/_build/html

# INSTALLERS

.PHONY: bin
bin:
	pyinstaller pyi/npc.spec
