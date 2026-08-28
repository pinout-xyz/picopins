# Raspberry Pi Pico GPIO Pinout

A beautiful GPIO pinout and pin function guide for the Raspberry Pi Pico, Pico W, Pico 2 and Pico 2 W.

![Example image](https://raw.githubusercontent.com/pinout-xyz/picopins/main/example.png)

[![Build Status](https://img.shields.io/github/actions/workflow/status/pinout-xyz/picopins/build.yml?branch=main)](https://github.com/pinout-xyz/picopins/actions/workflows/build.yml)
[![PyPi Package](https://img.shields.io/pypi/v/picopins.svg)](https://pypi.python.org/pypi/picopins)
[![Python Versions](https://img.shields.io/pypi/pyversions/picopins.svg)](https://pypi.python.org/pypi/picopins)

# Usage

```
usage: picopins [--...] [--all] or {spi,i2c,uart,pwm,hstx} [--find <text>]
       --pico          - Pico, the default. Or --picow, --pico2, --pico2w
       --pins          - show physical pin numbers
       --all or {spi,i2c,uart,pwm,hstx} - pick list of interfaces to show
                         hstx is Pico 2 and Pico 2 W only
       --hide-gpio     - hide GPIO pins
       --internal      - list the pins wired to onboard hardware
       --testpads      - list the underside test pads
       --light         - melt your eyeballs
       --find "<text>" - highlight pins matching <text>
                         supports regex if you're feeling sassy!

eg:    picopins i2c                    - show GPIO and I2C labels
       picopins                        - basic GPIO pinout
       picopins --pico2w --all         - everything, for a Pico 2 W
       picopins --picow --internal     - what the Pico W wires up itself
       picopins --all --find "PWM3 A"  - highlight any "PWM3 A" labels
       picopins --all --find "PWM.* A" - highlight any PWM A channels
```

The 40-pin header is identical across all four boards, apart from HSTX on
GP12-GP19 of the RP2350 boards. What differs is the hardware wired up behind
the scenes - `--internal` and `--testpads` show it.

# Installing

* Just run `python3 -m pip install picopins`

# Acknowledgements

This project was inspired by GPIO Zero's command-line pinout - https://github.com/gpiozero/gpiozero

It somehow wasn't inspired by Raspberry Pi Spy's "picopins" which came first and solves this same problem in bash - https://www.raspberrypi-spy.co.uk/2022/12/pi-pico-pinout-display-on-the-command-line/

Like RPi Spy's picopins it started as a GitHub gist, you can find the history here - https://gist.github.com/Gadgetoid/192af85a3eb05d4a6ac1db076c4ef118/revisions
