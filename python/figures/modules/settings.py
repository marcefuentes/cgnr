""" This file contains the settings for the figures. """

COLOR_MAP = "RdBu_r"
PLOT_SIZE = 4
SPACING = PLOT_SIZE * 0.75 / 4.0
LEFT_MARGIN = PLOT_SIZE * 2.5 / 4.0
RIGHT_MARGIN = PLOT_SIZE * 4.0 / 4.0
TOP_MARGIN = PLOT_SIZE * 2.5 / 4.0
BOTTOM_MARGIN = PLOT_SIZE * 2.5 / 4.0
LINE_WIDTH = PLOT_SIZE * 0.1 / 4.0
X_LABEL = r"Substitutability of $\it{B}$"
Y_LABEL = r"Influence of $\it{B}$"
X_LABEL_SIZE = PLOT_SIZE * 1.8 / 4.0
Y_LABEL_SIZE = PLOT_SIZE * 2.0 / 4.0
BIG_LABEL_SIZE = PLOT_SIZE * 9
LETTER_LABEL_SIZE = PLOT_SIZE * 8
LETTER_POSITION = 0.035
TITLE_PADDING = 11
TICK_LABEL_SIZE = PLOT_SIZE * 6
TICK_SIZE = PLOT_SIZE * 1.5
TICK_COLOR = "lightgrey"

# These is for results.py
PRINT_FOLDER = False

# N_X_VALUES must be 64 (BINS) for results.py
# It is also required for icurves.py
N_X_VALUES = 64

# These are for icurves.py
NC = 3
N_IC = 5
