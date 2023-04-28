# __TITLE__

[![Build Status](https://img.shields.io/github/actions/workflow/status/pimoroni/PROJECT_NAME-python/test.yml?branch=main)](https://github.com/pimoroni/PROJECT_NAME-python/actions/workflows/test.yml)
[![Coverage Status](https://coveralls.io/repos/github/pimoroni/PROJECT_NAME-python/badge.svg?branch=master)](https://coveralls.io/github/pimoroni/PROJECT_NAME-python?branch=master)
[![PyPi Package](https://img.shields.io/pypi/v/PROJECT_NAME.svg)](https://pypi.python.org/pypi/PROJECT_NAME)
[![Python Versions](https://img.shields.io/pypi/pyversions/PROJECT_NAME.svg)](https://pypi.python.org/pypi/PROJECT_NAME)

Generated from [the Pimoroni Python Boilerplate](https://github.com/pimoroni/boilerplate-python).

# Pre-requisites

You must enable (delete where appropriate):

* i2c: `sudo raspi-config nonint do_i2c 0`
* spi: `sudo raspi-config nonint do_spi 0`

You can optionally run `sudo raspi-config` or the graphical Raspberry Pi Configuration UI to enable interfaces.

# Installing

Stable library from PyPi:

* Just run `pip3 install PROJECT_NAME`

In some cases you may need to use `sudo` or install pip with: `sudo apt install python3-pip`

Latest/development library from GitHub:

* `git clone https://github.com/pimoroni/PROJECT_NAME-python`
* `cd PROJECT_NAME-python`
* `sudo ./install.sh`

