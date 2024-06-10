""" Data layouts. """


def curves(trait, mechanism=None, given=None):
    """Fitness curves for partner choice. """

    _ = given

    given_list = [["1.0"], ["0.5"]]

    variant = "nolang_noshuffle_cost15_4"

    if "Mimic" in trait:
        mechanism = "d"
    elif "Choose" in trait:
        mechanism = "p"

    layout = {
        "column_titles": [""],
        "givens": given_list,
        "givens_control": given_list,
        "mechanisms": [[mechanism], [mechanism]],
        "mechanisms_control": [["none"], ["none"]],
        "variants": [[variant], [variant]],
        "variants_control": [[variant], [variant]],
        "row_titles": ["", ""],
        "traits": [[trait], [trait]],
    }

    return layout


def figure_2(trait, mechanism=None, given=None):
    """Figure 2."""

    _ = given
    _ = mechanism

    given_list = [["1.0", "1.0"], ["0.5", "0.5"], ["0.0", "0.0"]]
    given_control_list = [[None, 0.0], [None, "0.0"], [None, "0.0"]]

    variant = "nolang_noshuffle_cost15_4"

    nrows = len(given_list)
    ncols = len(given_list[0])

    layout = {
        "column_titles": ["Fitness", "Fitness\nrelative to optimum"],
        "givens": given_list,
        "givens_control": given_control_list,
        "mechanisms": [["none", "none"] for _ in range(nrows)],
        "mechanisms_control": [[None, "none"] for _ in range(nrows)],
        "variants": [[variant for _ in range(ncols)] for _ in range(nrows)],
        "variants_control": [[variant for _ in range(ncols)] for _ in range(nrows)],
        "row_titles": ["", "", ""],
        "traits": [[trait, trait] for _ in range(nrows)],
    }

    return layout


def figure_3(trait, mechanism, given):
    """Figure 3 and subsequent ones."""

    variant_list = [
        ["nolang_noshuffle_cost15_128", "nolang_shuffle_cost15_128"],
        ["nolang_noshuffle_cost15_4", "nolang_shuffle_cost15_4"],
    ]

    nrows = len(variant_list)
    ncols = len(variant_list[0])

    layout = {
        "column_titles": ["No shuffling", "Shuffling"],
        "givens": [[given for _ in range(ncols)] for _ in range(nrows)],
        "givens_control": [[given for _ in range(ncols)] for _ in range(nrows)],
        "mechanisms": [[mechanism for _ in range(ncols)] for _ in range(nrows)],
        "mechanisms_control": [["none" for _ in range(ncols)] for _ in range(nrows)],
        "variants": variant_list,
        "variants_control": variant_list,
        "row_titles": ["", ""],
        "traits": [[trait for _ in range(ncols)] for _ in range(nrows)],
    }

    return layout


def theory(trait, mechanism=None, given=None):
    """First column is theoretical."""

    _ = given
    _ = mechanism

    given_list = [[None, "1.0"], [None, "0.5"], [None, "0.0"]]
    given_control_list = [[None, 0.0], [None, "0.0"], [None, "0.0"]]

    variant = [None, "nolang_noshuffle_cost15_4"]

    nrows = len(given_list)

    layout = {
        "column_titles": ["Fitness", "Fitness\nrelative to optimum"],
        "givens": given_list,
        "givens_control": given_control_list,
        "mechanisms": [[None, "none"] for _ in range(nrows)],
        "mechanisms_control": [[None, "none"] for _ in range(nrows)],
        "variants": [variant for _ in range(nrows)],
        "variants_control": [variant for _ in range(nrows)],
        "row_titles": ["", "", ""],
        "traits": [[None, trait] for _ in range(nrows)],
    }

    return layout
