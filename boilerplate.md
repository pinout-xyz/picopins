# Python Library Boilerplate <!-- omit in toc -->

Source: https://github.com/pimoroni/boilerplate-python

This Python Library boilerplate uses `pyproject.toml`, with a `hatchling` back-end.

`tox` is used to manage testing and QA, with `ruff` and `pytest`.

The tooling uses `build` as the front-end, but this is not essential. `python3 -m pip install .` will work just as well.

- [Get Started](#get-started)
- [Prepare Your Project](#prepare-your-project)
- [Linting](#linting)
- [Testing](#testing)
- [Examples](#examples)
- [Install / Uninstall Scripts](#install--uninstall-scripts)
- [Licensing](#licensing)
- [Git Remotes](#git-remotes)
- [Deployment](#deployment)

## Get Started

To get started, clone the contents of this repository.

You can also use it as a template, by starting here: https://github.com/pimoroni/boilerplate-python/generate

You should replace all instances of `PROJECT_NAME` with your project name. This should be a valid, Python package name. See: https://peps.python.org/pep-0008/#package-and-module-names

You can find outstanding replacements in your local copy with:

```
grep -Irn --color "__TITLE__"
grep -Irn --color "__DESCRIPTION__"
grep -Irn --color "PROJECT_NAME"
```

For the most part you will need to edit:

* `pyproject.toml` - pay attention to `authors` and `maintainers` and `keywords`
* `README.md` - title and introduce your project! Replace `pimoroni/PROJECT_NAME-python` with your own GitHub URL.
* `LICENSE` - update the license accordingly. You may relicense as you see fit.

Make sure you rename the `PROJECT_NAME` directory to match your chosen name.

A Makefile is provided to automate some tests, checks and package building. You should use it!

You should delete this file (`boilerplate.md`) from your project once you've set everything up.

## Prepare Your Project

* Create your Python library.
* Write at least *one* test.
* Write some examples!
* Fill out `CHANGELOG.md`

## Linting

You should ensure you either run `ruff` while writing the library, or use an IDE/Editor with linting.

All libraries (and example code) should stick to PEP8 style guides, although you can ignore long line warnings (E501) if you feel they're unwarranted.

You can run linting with `tox` by running:

```
make test-deps
make qa
```

`tox` will run `ruff`, in addition to `check-manifest` to ensure your GitHub repository and Python package are in sync, and `twine check` to ensure valid packages are being built. It will also run `codespell` to spell-check your code. Both `ruff` and `codespell` can be run from the project root, and will pick up configuration from `pyproject.toml` if you need faster checks while you work.

## Testing

At least one test script should be used to prevent obvious errors and omissions from creeping into the library.

You should use `tox` to run the test scripts:

```
make test-deps
make pytest
```

Make sure your main branch is named "main" or GitHub actions won't run!

## Examples

Examples should use hyphens and short, descriptive names, ie: `rainbow_larson.py`

Examples should include a `print()` front-matter introducing them, ie:

```python
print("""rainbow-larson.py - Display a larson scanning rainbow

Press Ctrl+C to exit.

""")
```

## Install / Uninstall Scripts

If your package directory (`PROJECT_NAME/`) differs from your library name, you should update `install.sh` and `uninstall.sh` and hard-code the correct library name.

## Licensing

This boilerplate should be considered CC-BY 4.0 - https://creativecommons.org/licenses/by/4.0/legalcode

The included MIT License is provided as an example (and because it's what we use, so it makes it easier to bootstrap our projects). You do not need to release projects based upon this boilerplate or modifications to the tools/scripts herein under the MIT License.

*However* you must provide attribution by means of a link to https://github.com/pimoroni/boilerplate-python in your `README.md`

## Git Remotes

If you have cloned `boilerplate-python` and want to point your local copy at a new git remote:

```
git remote rename origin boilerplate
git remote set-url --push boilerplate no_push
git remote add origin https://github.com/you_name/your_project
```

## Deployment

Before deploying you should `make testdeploy` and verify that the package looks good and is installable from test PyPi.

You can use `hatch version post` to bump the `.postN` version number if you need to make changes and preview them on test PyPi.

Make sure to *remove* the `.postN` version before release, the Makefile will try to check this for you.

You should also `make check` to catch common errors, including mismatched version numbers, trailing whitespace and DOS line-endings.

Before deployment you should `git tag -a "vX.X.X" -m "Version X.X.X"` (or `make tag`). Once you're happy with the release you can `git push origin master --follow-tags` to tag a release on GitHub that matches the deployed code. If you're using branch protection, we'll assume you know how to amend these commands!
