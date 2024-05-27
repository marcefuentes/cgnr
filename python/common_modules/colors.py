""" ANSI color codes for terminal output. """

COLORS = {
    "blue": "\033[94m",
    "cyan": "\033[96m",
    "green": "\033[32m",
    "red": "\033[91m",
    "purple": "\033[95m",
    "yellow": "\033[33m",
    "white": "\033[97m",
    "grey": "\033[90m",
    "bold": "\033[1m",
    "reset": "\033[0m",
}

ASK = {
    "yesno": f"{COLORS['bold']}{COLORS['green']}Yes{COLORS['reset']}/{COLORS['bold']}{COLORS['red']}No{COLORS['reset']}",
    "noyes": f"{COLORS['bold']}{COLORS['red']}Yes{COLORS['reset']}/{COLORS['bold']}{COLORS['green']}No{COLORS['reset']}",
}
