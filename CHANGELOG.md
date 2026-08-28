# Changelog

1.3.0
-----

* Add `--picow`, `--pico2` and `--pico2w` alongside the default `--pico`
* Add `hstx` interface for the RP2350 boards, numbered by bit
* Add `--internal` to list the pins wired to onboard hardware
* Add `--testpads` to list the underside test pads
* Draw the wireless module and relocated debug pads on the W boards

1.2.0
-----

* Add `--version`
* Make `--find GP25` and `--find LED` highlight the onboard LED
* Refactor options parsing into a class
* Pin a minimum `rich` version

1.1.0
-----

* Highlight GPIO label if `--find` matches a hidden label
* Add regex support to `--find`
* Rewrite render flow to make it less hacky
* Light mode is back! `--light`
* Move error text above usage message

1.0.1
-----

* Tidy up readme

1.0.0
-----

* Initial Release
* Ported from https://gist.github.com/Gadgetoid/192af85a3eb05d4a6ac1db076c4ef118
