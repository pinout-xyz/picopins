#!/bin/env python3
import re
import sys

import rich
from rich.panel import Panel
from rich.table import Table

"""
picopins, by @gadgetoid

Support me:
https://ko-fi.com/gadgetoid
https://github.com/sponsors/Gadgetoid
https://www.patreon.com/gadgetoid

Shout-out to Raspberry Pi Spy for having almost this exact idea first:
https://www.raspberrypi-spy.co.uk/2022/12/pi-pico-pinout-display-on-the-command-line/
"""

__version__ = '1.2.0'

PINOUT = [line.split("|") for line in """
      |      |         |        |        |      |  |     ┏━━━━━┓     |  |          |        |        |         |      |
      |      |         |        |        |      |  |┏━━━━┫     ┣━━━━┓|  |          |        |        |         |      |
      |PWM0 A|UART0 TX |I2C0 SDA|SPI0 RX |GP0   |1 |┃◎   ┗━━━━━┛   ◎┃|40|VBUS      |        |        |         |      |
      |PWM0 B|UART0 RX |I2C0 SCL|SPI0 CSn|GP1   |2 |┃◎ ▩           ◎┃|39|VSYS      |        |        |         |      |
      |      |         |        |        |Ground|3 |┃▣ └─GP25      ▣┃|38|Ground    |        |        |         |      |
      |PWM1 A|UART0 CTS|I2C1 SDA|SPI0 SCK|GP2   |4 |┃◎  ▒▒▒        ◎┃|37|3v3 En    |        |        |         |      |
      |PWM1 B|UART0 RTS|I2C1 SCL|SPI0 TX |GP3   |5 |┃◎  ▒▒▒        ◎┃|36|3v3 Out   |        |        |         |      |
      |PWM2 A|UART1 TX |I2C0 SDA|SPI0 RX |GP4   |6 |┃◎             ◎┃|35|ADC VRef  |        |        |         |      |
      |PWM2 B|UART1 RX |I2C0 SCL|SPI0 CSn|GP5   |7 |┃◎             ◎┃|34|GP28 / A2 |SPI1 RX |I2C0 SDA|UART0 TX |PWM6 A|
      |      |         |        |        |Ground|8 |┃▣             ▣┃|33|ADC Ground|        |        |         |      |
      |PWM3 A|UART1 CTS|I2C1 SDA|SPI0 SCK|GP6   |9 |┃◎   ▓▓▓▓▓▓▓   ◎┃|32|GP27 / A1 |SPI1 TX |I2C1 SCL|UART1 RTS|PWM5 B|
      |PWM3 B|UART1 RTS|I2C1 SCL|SPI0 TX |GP7   |10|┃◎   ▓▓▓▓▓▓▓   ◎┃|31|GP26 / A0 |SPI1 SCK|I2C1 SDA|UART1 CTS|PWM5 A|
      |PWM4 A|UART1 TX |I2C0 SDA|SPI1 RX |GP8   |11|┃◎   ▓▓▓▓▓▓▓   ◎┃|30|run       |        |        |         |      |
      |PWM4 B|UART1 RX |I2C0 SCL|SPI1 CSn|GP9   |12|┃◎   ▓▓▓▓▓▓▓   ◎┃|29|GP22      |SPI0 SCK|I2C1 SDA|UART1 CTS|PWM3 A|
      |      |         |        |        |Ground|13|┃▣             ▣┃|28|Ground    |        |        |         |      |
      |PWM5 A|UART1 CTS|I2C1 SDA|SPI1 SCK|GP10  |14|┃◎             ◎┃|27|GP21      |SPI0 CSn|I2C0 SCL|UART1 RX |PWM2 B|
      |PWM5 B|UART1 RTS|I2C1 SCL|SPI1 TX |GP11  |15|┃◎             ◎┃|26|GP20      |SPI0 RX |I2C0 SDA|UART1 TX |PWM2 A|
HSTX 0|PWM6 A|UART0 TX |I2C0 SDA|SPI1 RX |GP12  |16|┃◎             ◎┃|25|GP19      |SPI0 TX |I2C1 SCL|UART0 RTS|PWM1 B|HSTX 7
HSTX 1|PWM6 B|UART0 RX |I2C0 SCL|SPI1 CSn|GP13  |17|┃◎             ◎┃|24|GP18      |SPI0 SCK|I2C1 SDA|UART0 CTS|PWM1 A|HSTX 6
      |      |         |        |        |Ground|18|┃▣             ▣┃|23|Ground    |        |        |         |      |
HSTX 2|PWM7 A|UART0 CTS|I2C1 SDA|SPI1 SCK|GP14  |19|┃◎             ◎┃|22|GP17      |SPI0 CSn|I2C0 SCL|UART0 RX |PWM0 B|HSTX 5
HSTX 3|PWM7 B|UART0 RTS|I2C1 SCL|SPI1 TX |GP15  |20|┃◎    ◎ ▣ ◎    ◎┃|21|GP16      |SPI0 RX |I2C0 SDA|UART0 TX |PWM0 A|HSTX 4
      |      |         |        |        |      |  |┗━━━━━━━━━━━━━━━┛|  |          |        |        |         |      |
""".splitlines()[1:]]

DIAGRAM = [row[7] for row in PINOUT]
DIAGRAM_WIDTH = max(len(row) for row in DIAGRAM)

DIAGRAM_WIRELESS = """
     ┏━━━━━┓
┏━━━━┫     ┣━━━━┓
┃◎   ┗━━━━━┛   ◎┃
┃◎ ▩           ◎┃
┃▣ └─WL_GPIO0  ▣┃
┃◎  ▒▒▒        ◎┃
┃◎  ▒▒▒        ◎┃
┃◎             ◎┃
┃◎             ◎┃
┃▣             ▣┃
┃◎   ▓▓▓▓▓▓▓   ◎┃
┃◎   ▓▓▓▓▓▓▓   ◎┃
┃◎   ▓▓▓▓▓▓▓   ◎┃
┃◎   ▓▓▓▓▓▓▓   ◎┃
┃▣    ◎ ▣ ◎    ▣┃
┃◎  ░░░░░░░░░  ◎┃
┃◎  ░░░░░░░░░  ◎┃
┃◎  ░░░░░░░░░  ◎┃
┃◎  ░░░░░░░░░  ◎┃
┃▣  └─Wireless ▣┃
┃◎             ◎┃
┃◎             ◎┃
┗━━━━━━━━━━━━━━━┛
""".splitlines()[1:]

DIAGRAM_WIRELESS = [row.ljust(DIAGRAM_WIDTH) for row in DIAGRAM_WIRELESS]

LEFT_PINS = [[col.strip() for col in reversed(row[0:7])] for row in PINOUT]
RIGHT_PINS = [[col.strip() for col in row[8:]] for row in PINOUT]

ROWS = len(LEFT_PINS)
COLS = ["pins", "gpio", "spi", "i2c", "uart", "pwm", "hstx"]
COL_PIN_NUMS = 0
COL_GPIO = 1

LED_ROW = 3
WIRELESS_ROW = 19

POWER_PINS = [
    ("VSYS", "System voltage in/out", "5V out when USB powered (via a diode from VBUS), 1.8V to 5.5V in"),
    ("3v3 Out", "Chip 3v3 supply", "Can power external circuitry, keep the load under 300mA"),
]

INTERNAL_PINS = POWER_PINS + [
    ("GP23", "SMPS power-save", "LOW (default) for efficiency (PFM), HIGH for less ripple (PWM)"),
    ("GP24", "VBUS sense", "HIGH if USB or VBUS power is present"),
    ("GP25", "User LED", ""),
    ("GP29 / A3", "VSYS sense", "Reads VSYS/3 through a resistor divider"),
    ("A4", "Temperature", "Onboard temperature sensor"),
]

INTERNAL_PINS_WIRELESS = POWER_PINS + [
    ("GP23", "Wireless power on", ""),
    ("GP24", "Wireless SPI data / IRQ", ""),
    ("GP25", "Wireless SPI CSn", "Also enables the GP29 ADC when HIGH"),
    ("GP29 / A3", "Wireless SPI clock / VSYS sense", "Reads VSYS/3 through a resistor divider"),
    ("A4", "Temperature", "Onboard temperature sensor"),
    ("WL_GPIO0", "User LED", ""),
    ("WL_GPIO1", "SMPS power-save", "LOW (default) for efficiency (PFM), HIGH for less ripple (PWM)"),
    ("WL_GPIO2", "VBUS sense", "HIGH if USB or VBUS power is present"),
]

USB_TESTPADS = [
    ("TP1", "Ground", "Close-coupled ground for the differential USB signals"),
    ("TP2", "USB DM", "USB data negative"),
    ("TP3", "USB DP", "USB data positive"),
]

TESTPADS = USB_TESTPADS + [
    ("TP4", "GP23 / SMPS PS", "Marked do not use in the datasheet"),
    ("TP5", "GP25 / LED", "Only swings from 0V to the LED forward voltage"),
    ("TP6", "BOOTSEL", "Short low at power-up to boot into BOOTSEL"),
]

TESTPADS_WIRELESS = USB_TESTPADS + [
    ("TP4", "WL_GPIO1 / SMPS PS", "Marked do not use in the datasheet"),
    ("TP5", "WL_GPIO0 / LED", "Only swings from 0V to the LED forward voltage"),
    ("TP6", "BOOTSEL", "Short low at power-up to boot into BOOTSEL"),
]

BOARDS = {
    "pico": {
        "title": "Raspberry Pi Pico",
        "url": "https://pico.pinout.xyz",
        "diagram": DIAGRAM,
        "interfaces": ["spi", "i2c", "uart", "pwm"],
        "led": "GP25",
        "internal": INTERNAL_PINS,
        "testpads": TESTPADS,
    },
    "picow": {
        "title": "Raspberry Pi Pico W",
        "url": "https://picow.pinout.xyz",
        "diagram": DIAGRAM_WIRELESS,
        "interfaces": ["spi", "i2c", "uart", "pwm"],
        "led": "WL_GPIO0",
        "internal": INTERNAL_PINS_WIRELESS,
        "testpads": TESTPADS_WIRELESS,
    },
    "pico2": {
        "title": "Raspberry Pi Pico 2",
        "url": "https://pico2.pinout.xyz",
        "diagram": DIAGRAM,
        "interfaces": ["spi", "i2c", "uart", "pwm", "hstx"],
        "led": "GP25",
        "internal": INTERNAL_PINS,
        "testpads": TESTPADS + [
            ("TP7", "1V1", "Core voltage, marked do not use in the datasheet"),
        ],
    },
    "pico2w": {
        "title": "Raspberry Pi Pico 2 W",
        "url": "https://pico2w.pinout.xyz",
        "diagram": DIAGRAM_WIRELESS,
        "interfaces": ["spi", "i2c", "uart", "pwm", "hstx"],
        "led": "WL_GPIO0",
        "internal": INTERNAL_PINS_WIRELESS,
        "testpads": TESTPADS_WIRELESS,
    },
}

DEFAULT_BOARD = "pico"

THEME = {
    "gpio": "#859900",
    "pins": "#333333",
    "spi": "#d33682",
    "i2c": "#268bd2",
    "uart": "#6c71c4",
    "pwm": "#666666",
    "hstx": "#b58900",
    "panel": "#ffffff on #000000",
    "panel_light": "#000000 on #fdf6e3",
    "diagram": "#555555",
    "adc": "#2aa198",
    "power": "#dc322f",
    "ground": "#005b66",
    "run": "#df8f8e",
    "heading": "bold #859900",
    "notes": "#999999",
    "highlight": "bold #dc322f on white",
    "highlight_row": "bold {fg} on #444444"
}


def usage(error=None):
    error = f"\n[red]Error: {error}[/]\n" if error else ""
    rich.print(f"""
[#859900]picopins[/] [#2aa198]v{__version__}[/] - a beautiful GPIO pinout and pin function guide for the Raspberry Pi Pico
{error}
usage: picopins [--...] [--all] or {{{",".join(COLS[2:])}}} [--find <text>]
       --pico          - Pico, the default. Or --picow, --pico2, --pico2w
       --pins          - show physical pin numbers
       --all or {{{",".join(COLS[2:])}}} - pick list of interfaces to show
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

web:   https://pico.pinout.xyz
bugs:  https://github.com/pinout-xyz/picopins
""")
    sys.exit(1 if error else 0)


def gpio_style(pin):
    if pin in (3, 8, 13, 18, 23, 28, 38): return "ground"
    if pin in (40, 39, 37, 36): return "power"
    if pin in (35, 34, 33, 32, 31): return "adc"
    if pin == 30: return "run"
    return "gpio"


def styled(label, style, fg=None):
    style = THEME[style]
    style = style.format(fg=fg)
    return f'[{style}]{label}[/]'


def search(pin, highlight):
    if not highlight:
        return False
    # Hack to make "--find adc" also find A0, A1, etc
    if highlight.lower() == "adc":
        highlight += "|a[0-9]"
    highlight = re.compile(highlight, re.IGNORECASE)
    # Match search term against pin label
    return re.search(highlight, pin) is not None


def build_pins(pins, show_indexes, highlight=None):
    # Find all labels including the highlight word
    search_highlight = [search(pin, highlight) for pin in pins]
    # See if any non-visble labels match
    has_hidden_results = True in [index not in show_indexes and value
                                  for index, value in enumerate(search_highlight)]
    # Get the phyical pin for special case GPIO highlighting
    physical_pin_number = int(pins[COL_PIN_NUMS]) if pins[COL_PIN_NUMS] != "" else None
    # Iterate through the visible labels
    for i in show_indexes:
        label = pins[i]
        if search_highlight[i]:
            yield styled(label, "highlight")
        elif i == COL_GPIO:  # GPn / VSYS etc
            # Special case for styling power, ground, GPn, run, etc
            style = gpio_style(physical_pin_number)
            # Highlight for a non-visible search result
            if has_hidden_results:
                yield styled(label, "highlight_row", fg=THEME[style])
            else:
                yield styled(label, style)
        else:
            # Table column styles will catch the rest
            yield label


def build_row(row, diagram, show_indexes, highlight=None):
    for pin in build_pins(LEFT_PINS[row], show_indexes, highlight):
        yield pin + " "
    yield " " + diagram[row]
    # We can't reverse a generator
    for pin in reversed(list(build_pins(RIGHT_PINS[row], show_indexes, highlight))):
        yield " " + pin


def build_diagram(board, highlight=None):
    diagram = list(board["diagram"])
    led = board["led"]

    if search(f"{led} LED", highlight):
        diagram[LED_ROW] = diagram[LED_ROW].replace("▩", "[blink red]▩[/]")
        diagram[LED_ROW + 1] = diagram[LED_ROW + 1].replace(led, styled(led, "highlight"))

    if board["diagram"] is DIAGRAM_WIRELESS and search("Wireless", highlight):
        diagram[WIRELESS_ROW] = diagram[WIRELESS_ROW].replace("Wireless", styled("Wireless", "highlight"))

    return diagram


def build_extra(heading, rows, highlight=None):
    table = Table(
        title=styled(heading, "heading"),
        title_justify="left",
        box=None,
        pad_edge=False,
        expand=False,
        show_header=False)

    table.add_column(style=THEME["gpio"], no_wrap=True)
    table.add_column(style=THEME["adc"], no_wrap=True)
    table.add_column(style=THEME["notes"])

    for row in rows:
        table.add_row(*[styled(cell, "highlight") if search(cell, highlight) else cell for cell in row])

    return table


def picopins(opts):
    board = BOARDS[opts.board]
    show_indexes = []
    grid = Table.grid(expand=False)

    for label in reversed(opts.show):
        grid.add_column(justify="left", style=THEME[label], no_wrap=True)
        show_indexes.append(COLS.index(label))

    if opts.show_gpio:
        grid.add_column(justify="right", style=THEME["gpio"], no_wrap=True)
        show_indexes.append(COL_GPIO)

    if opts.show_pins:
        grid.add_column(justify="right", style=THEME["pins"], no_wrap=True)
        show_indexes.append(COL_PIN_NUMS)

    grid.add_column(no_wrap=True, style=THEME["diagram"])

    if opts.show_pins:
        grid.add_column(justify="left", style=THEME["pins"], no_wrap=True)

    if opts.show_gpio:
        grid.add_column(justify="left", style=THEME["gpio"], no_wrap=True)

    for label in opts.show:
        grid.add_column(justify="left", style=THEME[label], no_wrap=True)

    diagram = build_diagram(board, opts.find)

    for i in range(ROWS):
        grid.add_row(*build_row(i, diagram, show_indexes, highlight=opts.find))

    layout = Table.grid(expand=True)
    layout.add_row(grid)

    extras = []

    if opts.show_internal:
        extras.append(("Onboard hardware", board["internal"]))

    if opts.show_testpads:
        extras.append(("Test pads", board["testpads"]))

    for heading, rows in extras:
        layout.add_row("")
        layout.add_row(build_extra(heading, rows, opts.find))

    if extras:
        layout.add_row("")

    layout.add_row(f"@gadgetoid\n{board['url']}")

    return Panel(
        layout,
        title=f"{board['title']} Pinout",
        expand=False,
        style=THEME["panel_light"] if opts.light_mode else THEME["panel"])


class Options:
    def __init__(self, argv):
        argv.pop(0)

        if "--help" in argv:
            usage()

        if "--version" in argv:
            print(f"{__version__}")
            sys.exit(0)

        boards = [board for board in BOARDS if f"--{board}" in argv]

        if len(boards) > 1:
            usage("Please pick just one board.")

        self.board = boards[0] if boards else DEFAULT_BOARD
        self.interfaces = BOARDS[self.board]["interfaces"]

        self.all = "--all" in argv
        self.show_pins = "--pins" in argv
        self.show_gpio = "--hide-gpio" not in argv
        self.show_internal = "--internal" in argv
        self.show_testpads = "--testpads" in argv
        self.light_mode = "--light" in argv
        self.find = None

        if "--find" in argv:
            index = argv.index("--find") + 1
            if index >= len(argv) or argv[index].startswith("--"):
                usage("--find needs something to find.")
            self.find = argv.pop(index)

        # Assume any non -- args are labels
        self.show = [self.valid_label(arg) for arg in argv if not arg.startswith("--")]

        if self.show == [] and self.all:
            self.show = list(self.interfaces)
        elif self.all:
            usage("Please use either --all or a list of interfaces.")

    def valid_label(self, label):
        if label not in COLS[2:]:
            usage(f"Invalid interface \"{label}\".")
        if label not in self.interfaces:
            usage(f"\"{label}\" is not available on the {BOARDS[self.board]['title']}.")
        return label


def main():
    rich.print(picopins(Options(sys.argv)))


if __name__ == "__main__":
    main()
