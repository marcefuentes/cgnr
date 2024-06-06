""" Data layout. """


def figure_2():
    """ Figure 2. """

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
        "givens": [["1.0", "1.0"], ["0.5", "0.5"], ["0.0", "0.0"]],
        "givens_control": [[None, 0.0], [None, "0.0"], [None, "0.0"]],
        "mechanisms": [["none", "none"], ["none", "none"], ["none", "none"]],
        "mechanisms_control": [[None, "none"], [None, "none"], [None, "none"]],
        "variants": variant_list,
        "variants_control": variant_control_list,
        "row_titles": ["", ""],
    }

    return layout


def figure_3(mechanism, given):
    """ Figure 3 and subsequent ones. """

    variant_list = [
        ["nolang_noshuffle_cost15_128", "nolang_shuffle_cost15_128"],
        ["nolang_noshuffle_cost15_4", "nolang_shuffle_cost15_4"],
    ]

    nrows = len(variant_list)
    ncols = len(variant_list[0]) if nrows > 0 else 0

    layout = {
        "column_titles": ["No shuffling", "Shuffling"],
        "givens": [[given for _ in range(ncols)] for _ in range(nrows)],
        "givens_control": [[given for _ in range(ncols)] for _ in range(nrows)],
        "mechanisms": [[mechanism for _ in range(ncols)] for _ in range(nrows)],
        "mechanisms_control": [["none" for _ in range(ncols)] for _ in range(nrows)],
        "variants": variant_list,
        "variants_control": variant_list,
        "row_titles": ["", ""],
    }

    return layout


def p_fitness():
    """ Fitness curves for partner choice. """

    variant_list = [
        ["nolang_noshuffle_cost15_4", "nolang_noshuffle_cost15_4"],
    ]

    layout = {
        "column_titles": ["0.5", "1.0"],
        "givens": [["0.5", "1.0"]],
        "givens_control": [["0.5", "1.0"]],
        "mechanisms": [["p", "p"]],
        "mechanisms_control": [["none", "none"]],
        "variants": variant_list,
        "variants_control": variant_list,
        "row_titles": [""],
    }

    return layout


def get_data_layout(figure, mechanism, given):
    """ Get data layout for a figure. """

    if figure == "figure_2":
        return figure_2()
    elif figure == "figure_3":
        return figure_3(mechanism, given)
    elif figure == "p_fitness":
        return p_fitness()
    else:
        raise ValueError(f"Unknown figure: {figure}")
