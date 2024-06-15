""" Data layouts. """


def curves(options):
    """Fitness curves for partner choice."""

    variant = "nolang_noshuffle_cost15_4"
    given_list = [["1.0"], ["0.5"], ["0.0"]]
    trait = options["trait"]

    nrows = len(given_list)

    if "Mimic" in trait:
        mechanism = "d"
    elif "Choose" in trait:
        mechanism = "p"
    else:
        mechanism = options["mechanism"]

    layout = {
        "givens": given_list,
        "givens_control": given_list,
        "mechanisms": [[mechanism] for _ in range(nrows)],
        "mechanisms_control": [["none"] for _ in range(nrows)],
        "titles_columns": [""],
        "titles_rows": [""] * nrows,
        "traits": [[trait] for _ in range(nrows)],
        "variants": [[variant] for _ in range(nrows)],
        "variants_control": [[variant] for _ in range(nrows)],
    }

    return layout


def default(options):
    """Figure 3 and subsequent ones."""

    variant_list = [
        ["nolang_noshuffle_cost15_128", "nolang_shuffle_cost15_128"],
        ["nolang_noshuffle_cost15_4", "nolang_shuffle_cost15_4"],
    ]

    nrows = len(variant_list)
    ncols = len(variant_list[0])

    mechanisms = [[options["mechanism"] for _ in range(ncols)] for _ in range(nrows)]

    givens = [[options["given"] for _ in range(ncols)] for _ in range(nrows)]
    if options["mechanism_control"] == "social":
        mechanisms_control = [["none" for _ in range(ncols)] for _ in range(nrows)]
        givens_control = [["0.0" for _ in range(ncols)] for _ in range(nrows)]
    else:
        mechanisms_control = [[options["mechanism_control"] for _ in range(ncols)] for _ in range(nrows)]
        givens_control = [[options["given"] for _ in range(ncols)] for _ in range(nrows)]

    traits = [[options["trait"] for _ in range(ncols)] for _ in range(nrows)]

    layout = {
        "givens": givens,
        "givens_control": givens_control,
        "mechanisms": mechanisms,
        "mechanisms_control": mechanisms_control,
        "titles_columns": ["No shuffling", "Shuffling"],
        "titles_rows": [""] * nrows,
        "traits": traits,
        "variants": variant_list,
        "variants_control": variant_list,
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
        "givens": given_list,
        "givens_control": given_control_list,
        "mechanisms": [["none", "none"] for _ in range(nrows)],
        "mechanisms_control": [[None, "none"] for _ in range(nrows)],
        "titles_columns": ["Fitness", "Fitness\nrelative to optimum"],
        "titles_rows": [""] * nrows,
        "traits": [[trait, trait] for _ in range(nrows)],
        "variants": [[variant for _ in range(ncols)] for _ in range(nrows)],
        "variants_control": [[variant for _ in range(ncols)] for _ in range(nrows)],
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
        "givens": given_list,
        "givens_control": given_control_list,
        "mechanisms": [[None, "none"] for _ in range(nrows)],
        "mechanisms_control": [[None, "none"] for _ in range(nrows)],
        "titles_columns": ["Fitness\n(theory)", "Fitness\n(simulations)"],
        "titles_rows": [""] * nrows,
        "traits": [[None, trait] for _ in range(nrows)],
        "variants": [variant for _ in range(nrows)],
        "variants_control": [variant for _ in range(nrows)],
    }

    return layout
