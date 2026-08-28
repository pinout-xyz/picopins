LIBRARY_NAME := $(shell hatch project metadata name 2> /dev/null)
LIBRARY_VERSION := $(shell hatch version 2> /dev/null)

DEB_VERSION := $(shell sed -nE '1s/^[^(]*\(([^)]*)\).*/\1/p' debian/changelog 2> /dev/null)
CHANGELOG_VERSION := $(shell awk '/^[0-9]+\.[0-9]+\.[0-9]+$$/{print; exit}' CHANGELOG.md 2> /dev/null)

.PHONY: usage version dev-deps check pre-commit qa nopost tag build clean deb-deps deb
usage:
ifdef LIBRARY_NAME
	@echo "Library: ${LIBRARY_NAME}"
	@echo "Version: ${LIBRARY_VERSION}\n"
else
	@echo "WARNING: You should 'make dev-deps'\n"
endif
	@echo "Usage: make <target>, where target is one of:\n"
	@echo "dev-deps:     install Python dev dependencies"
	@echo "check:        verify CHANGELOG.md has an entry for the current version"
	@echo "qa:           run package QA (check-manifest, build, twine)"
	@echo "pre-commit:   run pre-commit hooks (lint, whitespace) on all files"
	@echo "clean:        clean Python build and dist directories"
	@echo "build:        build Python distribution files"
	@echo "tag:          tag the repository, eg: make tag VERSION=1.3.0"
	@echo "deb-deps:     install debian packaging dependencies"
	@echo "deb:          build a debian package\n"
	@echo "Releases are published to PyPi by .github/workflows/publish.yml,"
	@echo "triggered by publishing a GitHub release for the tag.\n"

version:
	@hatch version

dev-deps:
	uv sync
	uv run pre-commit install

check:
	@LIBRARY_VERSION=`hatch version | awk -F '.' '{print $$1"."$$2"."$$3}'`; \
	if grep -q "^$$LIBRARY_VERSION" CHANGELOG.md; then \
		echo "Changes found for version $$LIBRARY_VERSION."; \
	else \
		echo "Changes missing for version $$LIBRARY_VERSION! Please update CHANGELOG.md."; \
		exit 1; \
	fi
	@if [ "${CHANGELOG_VERSION}" = "${DEB_VERSION}" ]; then \
		echo "debian/changelog is at ${DEB_VERSION}."; \
	else \
		echo "debian/changelog is at ${DEB_VERSION}, CHANGELOG.md is at ${CHANGELOG_VERSION}! Please run dch -v ${CHANGELOG_VERSION}."; \
		exit 1; \
	fi

pre-commit:
	pre-commit run --all-files

qa:
	tox -e qa

nopost:
	@POST_VERSION=`hatch version | awk -F '.' '{print $$4}'`; \
	if [ -n "$$POST_VERSION" ]; then \
		echo "Found .$$POST_VERSION on library version; tag a release to build a clean version."; \
		exit 1; \
	fi

tag:
ifndef VERSION
	$(error Please specify a version, eg: make tag VERSION=1.3.0)
endif
	git tag -a "v${VERSION}" -m "Version ${VERSION}"

build:
	uv build

deb-deps:
	sudo apt-get install -y debhelper dh-python pybuild-plugin-pyproject python3-all \
		python3-hatchling python3-hatch-vcs python3-hatch-fancy-pypi-readme

deb:
	dpkg-buildpackage --build=binary --no-sign

clean:
	-rm -r dist
