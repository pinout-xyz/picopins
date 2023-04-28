#!/bin/env python3
import sys

from rich import print
from rich.panel import Panel
from rich.table import Table

"""
picopins, by @gadgetoid

Support me:
https://ko-fi.com/gadgetoid
https://github.com/sponsors/Gadgetoid
https://www.patreon.com/gadgetoid
"""

__version__ = '1.0.1'

pinout = [[col.strip() for col in line.split("|")] for line in """
      |         |        |        |      |  |     ┏━━━━━┓     |  |          |        |        |         |
      |         |        |        |      |  |┏━━━━┫     ┣━━━━┓|  |          |        |        |         |
PWM0 A|UART0 TX |I2C0 SDA|SPI0 RX |GP0   |1 |┃◎   ┗━━━━━┛   ◎┃|40|VBUS      |        |        |         |
PWM0 B|UART0 RX |I2C0 SCL|SPI0 CSn|GP1   |2 |┃◎ ▩           ◎┃|39|VSYS      |        |        |         |
      |         |        |        |Ground|3 |┃▣ └─GP25      ▣┃|38|Ground    |        |        |         |
PWM1 A|UART0 CTS|I2C1 SDA|SPI0 SCK|GP2   |4 |┃◎  ▒▒▒        ◎┃|37|3v3 En    |        |        |         |
PWM1 B|UART0 RTS|I2C1 SCL|SPI0 TX |GP3   |5 |┃◎  ▒▒▒        ◎┃|36|3v3 Out   |        |        |         |
PWM2 A|UART1 TX |I2C0 SDA|SPI0 RX |GP4   |6 |┃◎             ◎┃|35|ADC VRef  |        |        |         |
PWM2 B|UART1 RX |I2C0 SCL|SPI0 CSn|GP5   |7 |┃◎             ◎┃|34|GP28 / A2 |SPI1 RX |I2C0 SDA|UART0 TX |PWM6 A
      |         |        |        |Ground|8 |┃▣             ▣┃|33|ADC Ground|        |        |         |
PWM3 A|UART1 CTS|I2C1 SDA|SPI0 SCK|GP6   |9 |┃◎   ▓▓▓▓▓▓▓   ◎┃|32|GP27 / A1 |SPI1 TX |I2C1 SCL|UART1 RTS|PWM5 B
PWM3 B|UART1 RTS|I2C1 SCL|SPI0 TX |GP7   |10|┃◎   ▓▓▓▓▓▓▓   ◎┃|31|GP26 / A0 |SPI1 SCK|I2C1 SDA|UART1 CTS|PWM5 A
PWM4 A|UART1 TX |I2C0 SDA|SPI1 RX |GP8   |11|┃◎   ▓▓▓▓▓▓▓   ◎┃|30|run       |        |        |         |
PWM4 B|UART1 RX |I2C0 SCL|SPI1 CSn|GP9   |12|┃◎   ▓▓▓▓▓▓▓   ◎┃|29|GP22      |SPI0 SCK|I2C1 SDA|UART1 CTS|PWM3 A
      |         |        |        |Ground|13|┃▣             ▣┃|28|Ground    |        |        |         |
PWM5 A|UART1 CTS|I2C1 SDA|SPI1 SCK|GP10  |14|┃◎             ◎┃|27|GP21      |SPI0 CSn|I2C0 SCL|UART1 RX |PWM2 B
PWM5 B|UART1 RTS|I2C1 SCL|SPI1 TX |GP11  |15|┃◎             ◎┃|26|GP20      |SPI0 RX |I2C0 SDA|UART1 TX |PWM2 A
PWM6 A|UART0 TX |I2C0 SDA|SPI1 RX |GP12  |16|┃◎             ◎┃|25|GP19      |SPI0 TX |I2C1 SCL|UART0 RTS|PWM1 B
PWM6 B|UART0 RX |I2C0 SCL|SPI1 CSn|GP13  |17|┃◎             ◎┃|24|GP18      |SPI0 SCK|I2C1 SDA|UART0 CTS|PWM1 A
      |         |        |        |Ground|18|┃▣             ▣┃|23|Ground    |        |        |         |
PWM7 A|UART0 CTS|I2C1 SDA|SPI1 SCK|GP14  |19|┃◎             ◎┃|22|GP17      |SPI0 CSn|I2C0 SCL|UART0 RX |PWM0 B
PWM7 B|UART0 RTS|I2C1 SCL|SPI1 TX |GP15  |20|┃◎    ◎ ▣ ◎    ◎┃|21|GP16      |SPI0 RX |I2C0 SDA|UART0 TX |PWM0 A
      |         |        |        |      |  |┗━━━━━━━━━━━━━━━┛|  |          |        |        |         |
""".splitlines()[1:]]

COLS = ["spi", "i2c", "uart", "pwm"]

THEME = {
    "gpio": "#859900",
    "pins": "#333333",
    "spi": "#d33682",
    "i2c": "#268bd2",
    "uart": "#6c71c4",
    "pwm": "#666666",
    "panel": "#ffffff on #000000",
    "diagram": "#555555",
    "adc": "#2aa198",
    "power": "#dc322f",
    "ground": "#005b66",
    "run": "#df8f8e",
    "highlight": "#dc322f on white"
}


def usage(error=None):
    print(f"""
[#859900]picopins[/] [#2aa198]v{__version__}[/] - a beautiful GPIO pinout and pin function guide for the Raspberry Pi Pico
           Created by @gadgetoid - https://pico.pinout.xyz

usage: picopins [--pins] [--all] or {{{",".join(COLS)}}}
       --pins - show physical pin numbers
       --all or {{{",".join(COLS)}}} - pick list of interfaces to show
       --hide-gpio - hide GPIO pins
       --find "<text>" - highlight pins matching <text>

eg:    picopins i2c  - show GPIO and I2C labels
       picopins      - basic GPIO pinout
""")
    if error:
        print(f"[red]Error: {error}[/]")
    sys.exit(1 if error else 0)


def gpio_style(pin, label):
    style = THEME["gpio"]
    if pin in (3, 8, 13, 18, 23, 28, 38): style = THEME["ground"]
    if pin in (40, 39, 37, 36): style = THEME["power"]
    if pin in (35, 34, 33, 32, 31): style = THEME["adc"]
    if pin == 30: style = THEME["run"]
    return f'[{style}]{label}[/]'


def build_row(row, show_indexes, find=None):
    for index in show_indexes:
        label = row[index]
        # Special case styling for GPIO labels and search results
        if find and (find in label or find in label.lower()):
            label = f'[{THEME["highlight"]}]{label}[/]'
        else:
            if index == 4 and row[5] != "":
                label = gpio_style(int(row[5]), label)
            if index == 8 and row[7] != "":
                label = gpio_style(int(row[7]), label)
        # Slight fudge for whitespace between labels
        if index >= 6:
            label = " " + label
        if index <= 5:
            label = label + " "
        yield label


def valid_label(label):
    if label not in COLS:
        usage(f"Invalid interface \"{label}\"")
    return label


def main():
    if "--help" in sys.argv:
        usage()

    opts_all = "--all" in sys.argv
    opts_pins = "--pins" in sys.argv
    opts_hide_gpio = "--hide-gpio" in sys.argv

    if "--find" in sys.argv:
        index = sys.argv.index("--find") + 1
        opts_find = sys.argv[index]
        del sys.argv[index]
    else:
        opts_find = None

    opts_show = [valid_label(arg) for arg in sys.argv[1:] if not arg.startswith("--")]

    if opts_show == [] and opts_all:
        opts_show = COLS
    elif opts_all:
        usage("Please use either --all or a list of interfaces.")


    show_indexes = []
    grid = Table.grid(expand=True)

    for label in reversed(opts_show):
        grid.add_column(justify="left", style=THEME[label], no_wrap=True)
        show_indexes.append(list(reversed(COLS)).index(label))

    if not opts_hide_gpio:
        grid.add_column(justify="right", style=THEME["gpio"], no_wrap=True)
        show_indexes += [4]

    if opts_pins:
        grid.add_column(justify="right", style=THEME["pins"], no_wrap=True)
        show_indexes += [5]

    grid.add_column(justify="center", no_wrap=True, style=THEME["diagram"])
    show_indexes += [6]

    if opts_pins:
        grid.add_column(justify="left", style=THEME["pins"], no_wrap=True)
        show_indexes += [7]

    if not opts_hide_gpio:
        grid.add_column(justify="left", style=THEME["gpio"], no_wrap=True)
        show_indexes += [8]

    for label in opts_show:
        grid.add_column(justify="left", style=THEME[label], no_wrap=True)
        show_indexes.append(9 + COLS.index(label))

    for row in pinout:
        grid.add_row(*build_row(row, show_indexes, find=opts_find))

    layout = Table.grid(expand=True)
    layout.add_row(grid)
    layout.add_row("@gadgetoid\nhttps://pico.pinout.xyz")

    print(Panel(
        layout,
        title="Raspberry Pi Pico Pinout",
        expand=False,
        style=THEME["panel"]))


if __name__ == "__main__":
    main()
