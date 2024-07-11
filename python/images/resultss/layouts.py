""" Data layouts. """


def allp(options):
    """All figures."""

    lang = "lang" if options["lang"] else "nolang"

    variant_list = [
        f"{lang}_noshuffle_cost15_4",
        f"{lang}_noshuffle_cost15_128",
        f"{lang}_shuffle_cost15_4",
        f"{lang}_shuffle_cost15_128",
    ]

    ncols = len(variant_list)

    mechanism_list = ["p", "d", "i", "pd", "pi"]
    # mechanism_list = ["i", "pi"]
    mechanisms = [[mech for _ in range(ncols)] for mech in mechanism_list]

    nrows = len(mechanism_list)

    variants = [variant_list for _ in range(nrows)]

    layout = {
        "givens": repeat_for_matrix(options["given"], nrows, ncols),
        "givens_control": repeat_for_matrix(options["given_control"], nrows, ncols),
        "mechanisms": mechanisms,
        "mechanisms_control": repeat_for_matrix("none", nrows, ncols),
        "titles_columns": [
            "No shuffling\n4",
            "No shuffling\n128",
            "Shuffling\n4",
            "Shuffling\n128",
        ],
        "titles_rows": mechanism_list,
        "traits": repeat_for_matrix(options["trait"], nrows, ncols),
        "traits_control": repeat_for_matrix(options["trait"], nrows, ncols),
        "variants": variants,
        "variants_control": variants,
    }

    return layout


def curves(options):
    """Fitness curves for partner choice."""

    given_list = [["1.0"], ["0.5"], ["0.0"]]

    nrows = len(given_list)

    if "Mimic" in options["trait"]:
        mechanism = "d"
    elif "Choose" in options["trait"]:
        mechanism = "p"
    else:
        mechanism = options["mechanism"]

    traits = repeat_for_matrix(options["trait"], nrows, 1)
    variants = repeat_for_matrix("nolang_noshuffle_cost15_4", nrows, 1)

    layout = {
        "givens": given_list,
        "givens_control": given_list,
        "mechanisms": repeat_for_matrix(mechanism, nrows, 1),
        "mechanisms_control": repeat_for_matrix("none", nrows, 1),
        "titles_columns": [""],
        "titles_rows": [""] * nrows,
        "traits": traits,
        "traits_control": traits,
        "variants": variants,
        "variants_control": variants,
    }

    return layout


def custom(options):
    """Custom."""

    variant_list = [
        [
            "nolang_noshuffle_cost15_128",
            "lang_noshuffle_cost15_128",
            "nolang_shuffle_cost15_128",
            "lang_shuffle_cost15_128",
        ],
        [
            "nolang_noshuffle_cost15_128",
            "lang_noshuffle_cost15_128",
            "nolang_shuffle_cost15_128",
            "lang_shuffle_cost15_128",
        ],
        [
            "nolang_noshuffle_cost15_4",
            "lang_noshuffle_cost15_4",
            "nolang_shuffle_cost15_4",
            "lang_shuffle_cost15_4",
        ],
        [
            "nolang_noshuffle_cost15_4",
            "lang_noshuffle_cost15_4",
            "nolang_shuffle_cost15_4",
            "lang_shuffle_cost15_4",
        ],
    ]

    titles_columns = [
        "No shuffling\nShort memory",
        "No shuffling\nLong memory",
        "Shuffling\nShort memory",
        "Shuffling\nLong memory",
    ]

    nrows = len(variant_list)
    ncols = len(variant_list[0])

    mechanisms = [
        ["pd", "pd", "pd", "pd"],
        ["pi", "pi", "pi", "pi"],
        ["pd", "pd", "pd", "pd"],
        ["pi", "pi", "pi", "pi"],
    ]

    layout = {
        "givens": repeat_for_matrix(options["given"], nrows, ncols),
        "givens_control": repeat_for_matrix(options["given_control"], nrows, ncols),
        "mechanisms": mechanisms,
        "mechanisms_control": repeat_for_matrix("none", nrows, ncols),
        "titles_columns": titles_columns,
        "titles_rows": [""] * nrows,
        "traits": repeat_for_matrix(options["trait"], nrows, ncols),
        "traits_control": repeat_for_matrix(options["trait_control"], nrows, ncols),
        "variants": variant_list,
        "variants_control": variant_list,
    }

    return layout


def default(options):
    """Figure 3 and subsequent ones."""

    lang = "lang" if options["lang"] else "nolang"

    variant_list = [
        [f"{lang}_noshuffle_cost15_128", f"{lang}_shuffle_cost15_128"],
        [f"{lang}_noshuffle_cost15_4", f"{lang}_shuffle_cost15_4"],
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
        givens_control = repeat_for_matrix(options["given_control"], nrows, ncols)

    traits = repeat_for_matrix(options["trait"], nrows, ncols)

    layout = {
        "givens": repeat_for_matrix(options["given"], nrows, ncols),
        "givens_control": givens_control,
        "mechanisms": repeat_for_matrix(options["mechanism"], nrows, ncols),
        "mechanisms_control": mechanisms_control,
        "titles_columns": ["No shuffling", "Shuffling"],
        "titles_rows": [""] * nrows,
        "traits": traits,
        "traits_control": traits,
        "variants": variant_list,
        "variants_control": variant_list,
    }

    return layout


def dilemmas(options):
    """Magnitud of social dilemmas."""

    given_list = [["1.0", "1.0"], ["0.5", "0.5"], ["0.0", "0.0"]]

    nrows = len(given_list)
    ncols = len(given_list[0])

    trait_list = [["qBSeenmean", "wmean"] for _ in range(nrows)]

    layout = {
        "givens": given_list,
        "givens_control": repeat_for_matrix("0.0", nrows, ncols),
        "mechanisms": repeat_for_matrix(options["mechanism"], nrows, ncols),
        "mechanisms_control": repeat_for_matrix(
            options["mechanism_control"], nrows, ncols
        ),
        "titles_columns": ["$\\mathit{q}_{\\mathit{B}}$", "Fitness"],
        "titles_rows": [""] * nrows,
        "traits": trait_list,
        "traits_control": trait_list,
        "variants": repeat_for_matrix("nolang_noshuffle_cost15_4", nrows, ncols),
        "variants_control": repeat_for_matrix(
            "nolang_noshuffle_cost15_4", nrows, ncols
        ),
    }

    return layout


def figure_2(options):
    """Figure 2."""

    given_list = [["1.0", "1.0"], ["0.5", "0.5"], ["0.0", "0.0"]]
    given_control_list = [[None, "0.0"], [None, "0.0"], [None, "0.0"]]

    nrows = len(given_list)
    ncols = len(given_list[0])

    mechanisms_control = [[None, "none"] for _ in range(nrows)]
    traits = repeat_for_matrix(options["trait"], nrows, ncols)
    variants = repeat_for_matrix("nolang_noshuffle_cost15_4", nrows, ncols)

    layout = {
        "givens": given_list,
        "givens_control": given_control_list,
        "mechanisms": repeat_for_matrix("none", nrows, ncols),
        "mechanisms_control": mechanisms_control,
        "titles_columns": ["Fitness", "Fitness\nrelative to optimum"],
        "titles_rows": [""] * nrows,
        "traits": traits,
        "traits_control": traits,
        "variants": variants,
        "variants_control": variants,
    }

    return layout


def repeat_for_matrix(value, nrows, ncols):
    """Repeat a value for a matrix."""

    return [[value for _ in range(ncols)] for _ in range(nrows)]


def single_column(options):
    """Single column."""

    lang = "lang" if options["lang"] else "nolang"

    variant_list = [
        [f"{lang}_shuffle_cost15_128"],
        [f"{lang}_shuffle_cost15_4"],
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
        givens_control = repeat_for_matrix(options["given_control"], nrows, ncols)

    traits = repeat_for_matrix(options["trait"], nrows, ncols)

    layout = {
        "givens": repeat_for_matrix(options["given"], nrows, ncols),
        "givens_control": givens_control,
        "mechanisms": repeat_for_matrix(options["mechanism"], nrows, ncols),
        "mechanisms_control": mechanisms_control,
        "titles_columns": ["Shuffling"],
        "titles_rows": [""] * nrows,
        "traits": traits,
        "traits_control": traits,
        "variants": variant_list,
        "variants_control": variant_list,
    }

    return layout


def sss(options):
    """Different combinations of reciprocity."""

    variant_list = [
        ["nolang_shuffle_cost15_128", "nolang_shuffle_cost15_128", "lang_shuffle_cost15_128"],
        ["nolang_shuffle_cost15_4", "nolang_shuffle_cost15_4", "lang_shuffle_cost15_4"],
    ]

    nrows = len(variant_list)
    ncols = len(variant_list[0])

    mechanisms = [["d", "i", "i"], ["d", "i", "i"]]
    traits = repeat_for_matrix(options["trait"], nrows, ncols)

    titles = [ 
        "$\\mathit{s}_{\\mathit{1}}$",
        "$\\mathit{s}_{\\mathit{1}}$, $\\mathit{s}_{\\mathit{2}}$",
        "$\\mathit{s}_{\\mathit{1}}$, $\\mathit{s}_{\\mathit{2}}$, $\\mathit{s}_{\\mathit{3}}$",
    ]

    layout = {
        "givens": repeat_for_matrix(options["given"], nrows, ncols),
        "givens_control": repeat_for_matrix(options["given_control"], nrows, ncols),
        "mechanisms": mechanisms,
        "mechanisms_control": repeat_for_matrix(options["mechanism_control"], nrows, ncols),
        "titles_columns": titles,
        "titles_rows": [""] * nrows,
        "traits": traits,
        "traits_control": traits,
        "variants": variant_list,
        "variants_control": variant_list,
    }

    return layout


def theory(options):
    """First column is theoretical."""

    given_list = [[None, "1.0"], [None, "0.5"], [None, "0.0"]]

    nrows = len(given_list)

    mechanisms = [[None, "none"] for _ in range(nrows)]
    traits = [[None, options["trait"]] for _ in range(nrows)]
    variants = [[None, "nolang_noshuffle_cost15_4"] for _ in range(nrows)]

    layout = {
        "givens": given_list,
        "givens_control": repeat_for_matrix(None, nrows, 2),
        "mechanisms": mechanisms,
        "mechanisms_control": mechanisms,
        "titles_columns": ["Fitness\n(theory)", "Fitness\n(simulations)"],
        "titles_rows": [""] * nrows,
        "traits": traits,
        "traits_control": traits,
        "variants": variants,
        "variants_control": variants,
    }

    return layout


def unit(options):
    """Single plot."""

    lang = "lang" if options["lang"] else "nolang"

    variant_list = [[f"{lang}_noshuffle_cost15_4"]]

    layout = {
        "givens": [[options["given"]]],
        "givens_control": [["0.0"]],
        "mechanisms": [[options["mechanism"]]],
        "mechanisms_control": [[options["mechanism_control"]]],
        "titles_columns": ["No shuffling"],
        "titles_rows": [""],
        "traits": [[options["trait"]]],
        "traits_control": [[options["trait_control"]]],
        "variants": variant_list,
        "variants_control": variant_list,
    }

    return layout
