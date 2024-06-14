""" Data layouts. """


def curves(options):
    """Fitness curves for partner choice."""

    variant = "nolang_noshuffle_cost15_4"
    given_list = [["1.0"], ["0.5"]]
    trait = options["trait"]

    if "Mimic" in trait:
        mechanism = "d"
    elif "Choose" in trait:
        mechanism = "p"
    else:
        mechanism = options["mechanism"]

    layout = {
        "titles_columns": [""],
        "givens": given_list,
        "givens_control": given_list,
        "mechanisms": [[mechanism], [mechanism]],
        "mechanisms_control": [["none"], ["none"]],
        "variants": [[variant], [variant]],
        "variants_control": [[variant], [variant]],
        "titles_rows": ["", ""],
        "traits": [[trait], [trait]],
    }

    return layout


def figure_2(options):
    """Figure 2."""

    variant = "nolang_noshuffle_cost15_4"
    given_list = [["1.0", "1.0"], ["0.5", "0.5"], ["0.0", "0.0"]]
    given_control_list = [[None, 0.0], [None, "0.0"], [None, "0.0"]]
    trait = options["trait"]

    nrows = len(given_list)
    ncols = len(given_list[0])

    layout = {
        "titles_columns": ["Fitness", "Fitness\nrelative to optimum"],
        "givens": given_list,
        "givens_control": given_control_list,
        "mechanisms": [["none", "none"] for _ in range(nrows)],
        "mechanisms_control": [[None, "none"] for _ in range(nrows)],
        "variants": [[variant for _ in range(ncols)] for _ in range(nrows)],
        "variants_control": [[variant for _ in range(ncols)] for _ in range(nrows)],
        "titles_rows": ["", "", ""],
        "traits": [[trait, trait] for _ in range(nrows)],
    }

    return layout


def figure_3(options):
    """Figure 3 and subsequent ones."""

    variant_list = [
        ["nolang_noshuffle_cost15_128", "nolang_shuffle_cost15_128"],
        ["nolang_noshuffle_cost15_4", "nolang_shuffle_cost15_4"],
    ]
    mechanism = options["mechanism"]
    given = options["given"]
    trait = options["trait"]

    nrows = len(variant_list)
    ncols = len(variant_list[0])

    layout = {
        "titles_columns": ["No shuffling", "Shuffling"],
        "givens": [[given for _ in range(ncols)] for _ in range(nrows)],
        "givens_control": [[given for _ in range(ncols)] for _ in range(nrows)],
        "mechanisms": [[mechanism for _ in range(ncols)] for _ in range(nrows)],
        "mechanisms_control": [["none" for _ in range(ncols)] for _ in range(nrows)],
        "variants": variant_list,
        "variants_control": variant_list,
        "titles_rows": ["", ""],
        "traits": [[trait for _ in range(ncols)] for _ in range(nrows)],
    }

    return layout


def theory(options):
    """First column is theoretical."""

    variant = [None, "nolang_noshuffle_cost15_4"]
    given_list = [[None, "1.0"], [None, "0.5"], [None, "0.0"]]
    given_control_list = [[None, None], [None, None], [None, None]]
    trait = options["trait"]

    nrows = len(given_list)

    layout = {
        "titles_columns": ["Fitness\n(theory)", "Fitness\n(simulations)"],
        "givens": given_list,
        "givens_control": given_control_list,
        "mechanisms": [[None, "none"] for _ in range(nrows)],
        "mechanisms_control": [[None, "none"] for _ in range(nrows)],
        "variants": [variant for _ in range(nrows)],
        "variants_control": [variant for _ in range(nrows)],
        "titles_rows": ["", "", ""],
        "traits": [[None, trait] for _ in range(nrows)],
    }

    return layout
