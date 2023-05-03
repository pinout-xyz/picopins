# Raspberry Pi Pico GPIO Pinout

A beautiful GPIO pinout and pin function guide for the Raspberry Pi Pico.

![Example image](https://raw.githubusercontent.com/pinout-xyz/picopins/main/example.png)

[![Build Status](https://img.shields.io/github/actions/workflow/status/pinout-xyz/picopins/build.yml?branch=main)](https://github.com/pinout-xyz/picopins/actions/workflows/build.yml)
[![PyPi Package](https://img.shields.io/pypi/v/picopins.svg)](https://pypi.python.org/pypi/picopins)
[![Python Versions](https://img.shields.io/pypi/pyversions/picopins.svg)](https://pypi.python.org/pypi/picopins)

# Usage

```
usage: picopins [--pins] [--all] or {spi,i2c,uart,pwm}
       --pins - show physical pin numbers
       --all or {spi,i2c,uart,pwm} - pick list of interfaces to show
       --hide-gpio - hide GPIO pins
       --find "<text>" - highlight pins matching <text>

eg:    picopins i2c  - show GPIO and I2C labels
       picopins      - basic GPIO pinout
```

# Installing

* Just run `python3 -m pip install picopins`

# Acknowledgements

This project was inspired by GPIO Zero's command-line pinout - https://github.com/gpiozero/gpiozero

It somehow wasn't inspired by Raspberry Pi Spy's "picopins" which came first and solves this same problem in bash - https://www.raspberrypi-spy.co.uk/2022/12/pi-pico-pinout-display-on-the-command-line/

Like RPi Spy's picopins it started as a GitHub gist, you can find the history here - https://gist.github.com/Gadgetoid/192af85a3eb05d4a6ac1db076c4ef118/revisions
