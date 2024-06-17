""" Data layouts. """


def curves(options):
    """Fitness curves for partner choice."""

    variant = "nolang_noshuffle_cost15_4"
    given_list = [["1.0"], ["0.5"], ["0.0"]]

    nrows = len(given_list)

    variants = repeat_for_matrix(variant, nrows, 1)

    if "Mimic" in options["trait"]:
        mechanism = "d"
    elif "Choose" in options["trait"]:
        mechanism = "p"
    else:
        mechanism = options["mechanism"]

    layout = {
        "givens": given_list,
        "givens_control": given_list,
        "mechanisms": repeat_for_matrix(mechanism, nrows, 1),
        "mechanisms_control": repeat_for_matrix("none", nrows, 1),
        "titles_columns": [""],
        "titles_rows": [""] * nrows,
        "traits": repeat_for_matrix(options["trait"], nrows, 1),
        "variants": variants,
        "variants_control": variants,
    }

    return layout


def default(options):
    """Figure 3 and subsequent ones."""

    variant_list = [
        ["lang_noshuffle_cost15_128", "lang_shuffle_cost15_128"],
        ["lang_noshuffle_cost15_4", "lang_shuffle_cost15_4"],
    ]

    nrows = len(variant_list)
    ncols = len(variant_list[0])

    if options["mechanism_control"] == "social":
        mechanisms_control = repeat_for_matrix("none", nrows, ncols)
        givens_control = repeat_for_matrix("0.0", nrows, ncols)
    else:
        mechanisms_control = repeat_for_matrix(
            options["mechanism_control"], nrows, ncols
        )
        givens_control = repeat_for_matrix(options["given"], nrows, ncols)

    layout = {
        "givens": repeat_for_matrix(options["given"], nrows, ncols),
        "givens_control": givens_control,
        "mechanisms": repeat_for_matrix(options["mechanism"], nrows, ncols),
        "mechanisms_control": mechanisms_control,
        "titles_columns": ["No shuffling", "Shuffling"],
        "titles_rows": [""] * nrows,
        "traits": repeat_for_matrix(options["trait"], nrows, ncols),
        "variants": variant_list,
        "variants_control": variant_list,
    }

    return layout


def figure_2(options):
    """Figure 2."""

    variant = "nolang_noshuffle_cost15_4"
    given_list = [["1.0", "1.0"], ["0.5", "0.5"], ["0.0", "0.0"]]
    given_control_list = [[None, "0.0"], [None, "0.0"], [None, "0.0"]]

    nrows = len(given_list)
    ncols = len(given_list[0])

    variants = repeat_for_matrix(variant, nrows, ncols)
    mechanisms_control = [[None, "none"] for _ in range(nrows)]

    layout = {
        "givens": given_list,
        "givens_control": given_control_list,
        "mechanisms": repeat_for_matrix("none", nrows, ncols),
        "mechanisms_control": mechanisms_control,
        "titles_columns": ["Fitness", "Fitness\nrelative to optimum"],
        "titles_rows": [""] * nrows,
        "traits": repeat_for_matrix(options["trait"], nrows, ncols),
        "variants": variants,
        "variants_control": variants,
    }

    return layout


def repeat_for_matrix(value, nrows, ncols):
    """Repeat a value for a matrix."""

    return [[value for _ in range(ncols)] for _ in range(nrows)]


def theory(options):
    """First column is theoretical."""

    variant = [None, "nolang_noshuffle_cost15_4"]
    given_list = [[None, "1.0"], [None, "0.5"], [None, "0.0"]]

    nrows = len(given_list)

    variants = [variant for _ in range(nrows)]
    mechanisms = [[None, "none"] for _ in range(nrows)]
    traits = [[None, options["trait"]] for _ in range(nrows)]

    layout = {
        "givens": given_list,
        "givens_control": repeat_for_matrix(None, nrows, 2),
        "mechanisms": mechanisms,
        "mechanisms_control": mechanisms,
        "titles_columns": ["Fitness\n(theory)", "Fitness\n(simulations)"],
        "titles_rows": [""] * nrows,
        "traits": traits,
        "variants": variants,
        "variants_control": variants,
    }

    return layout
