""" Data layout. """


def figure_2():
    """ Data layout for Figure 2. """

    variant_list = [
        ["nolang_noshuffle_cost15_4", "nolang_noshuffle_cost15_4"],
        ["nolang_noshuffle_cost15_4", "nolang_noshuffle_cost15_4"],
        ["nolang_noshuffle_cost15_4", "nolang_noshuffle_cost15_4"],
    ]

    variant_control_list = [
        [None, "nolang_noshuffle_cost15_4"],
        [None, "nolang_noshuffle_cost15_4"],
        [None, "nolang_noshuffle_cost15_4"],
    ]

    layout = {
        "column_titles": ["Fitness", "Fitness\nrelative to optimum"],
        "folder_given": [["1.0", "1.0"], ["0.5", "0.5"], ["0.0", "0.0"]],
        "folder_given_control": [[None, 0.0], [None, "0.0"], [None, "0.0"]],
        "folder_mechanism": [["none", "none"], ["none", "none"], ["none", "none"]],
        "folder_mechanism_control": [[None, "none"], [None, "none"], [None, "none"]],
        "folder_variant": variant_list,
        "folder_variant_control": variant_control_list,
        "given": "",
        "row_titles": ["", ""],
    }

    return layout


def figure_3(mechanism, given):
    """ Data layout for Figure 3 and subsequent ones. """

    variant_list = [
        ["nolang_noshuffle_cost15_128", "nolang_shuffle_cost15_128"],
        ["nolang_noshuffle_cost15_4", "nolang_shuffle_cost15_4"],
    ]

    nrows = len(variant_list)
    ncols = len(variant_list[0]) if nrows > 0 else 0

    layout = {
        "column_titles": ["No shuffling", "Shuffling"],
        "folder_given": [[given for _ in range(ncols)] for _ in range(nrows)],
        "folder_given_control": [[given for _ in range(ncols)] for _ in range(nrows)],
        "folder_mechanism": [[mechanism for _ in range(ncols)] for _ in range(nrows)],
        "folder_mechanism_control": [["none" for _ in range(ncols)] for _ in range(nrows)],
        "folder_variant": variant_list,
        "folder_variant_control": variant_list,
        "given": given,
        "row_titles": ["", ""],
    }

    return layout


def get_data_layout(figure, mechanism, given):
    """ Get data layout for a figure. """

    if figure == "figure_2":
        return figure_2()
    elif figure == "figure_3":
        return figure_3(mechanism, given)
    else:
        raise ValueError(f"Unknown figure: {figure}")
