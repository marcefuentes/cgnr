""" Data layouts. """


def all16(options):
    """All figures."""

    lang = "lang" if options["lang"] else "nolang"

    variants = [
        [
            f"{lang}_noshuffle_cost15_128",
            f"{lang}_noshuffle_cost15_128",
            f"{lang}_shuffle_cost15_128",
            f"{lang}_shuffle_cost15_128",
        ],
        [
            f"{lang}_noshuffle_cost15_4",
            f"{lang}_noshuffle_cost15_4",
            f"{lang}_shuffle_cost15_4",
            f"{lang}_shuffle_cost15_4",
        ],
        [
            f"{lang}_noshuffle_cost15_128",
            f"{lang}_noshuffle_cost15_128",
            f"{lang}_shuffle_cost15_128",
            f"{lang}_shuffle_cost15_128",
        ],
        [
            f"{lang}_noshuffle_cost15_4",
            f"{lang}_noshuffle_cost15_4",
            f"{lang}_shuffle_cost15_4",
            f"{lang}_shuffle_cost15_4",
        ],
    ]

    nrows = len(variants)
    ncols = len(variants[0])

    givens = [
        ["1.0", "1.0", "1.0", "1.0"],
        ["1.0", "1.0", "1.0", "1.0"],
        ["0.5", "0.5", "0.5", "0.5"],
        ["0.5", "0.5", "0.5", "0.5"],
    ]
    
    givens_control = givens
    givens_control = repeat_for_matrix("0.0", nrows, ncols)

    mechanisms = [["pd", "pi", "pd", "pi"] for _ in range(nrows)]

    if "Imimic" in options["trait"]:
        traits = [[None, options["trait"], None, options["trait"]] for _ in range(nrows)]
    else:
        traits = repeat_for_matrix(options["trait"], nrows, ncols)

    s1 = "$\\mathit{s}_{\\mathit{1}}$"
    s2 = "$\\mathit{s}_{\\mathit{2}}$"
    s3 = "$\\mathit{s}_{\\mathit{3}}$"
    s4 = "$\\mathit{s}_{\\mathit{4}}$"
    s5 = "$\\mathit{s}_{\\mathit{5}}$"

    titles_columns = [
        f"No shuffling\n{s1}, {s4}",
        f"No shuffling\n{s1}, {s2}, {s4}",
        f"Shuffling\n{s1}, {s4}",
        f"Shuffling\n{s1}, {s2}, {s4}",
    ]

    layout = {
        "givens": givens,
        "givens_control": givens_control,
        "mechanisms": mechanisms,
        "mechanisms_control": repeat_for_matrix("none", nrows, ncols),
        "titles_columns": titles_columns,
        "titles_rows": [""] * nrows,
        "traits": traits,
        "traits_control": traits,
        "variants": variants,
        "variants_control": variants,
    }

    return layout


def all8(options):
    """All figures."""

    lang = "lang" if options["lang"] else "nolang"

    variants = [
        [
            f"{lang}_noshuffle_cost15_128",
            f"{lang}_noshuffle_cost15_128",
            f"{lang}_shuffle_cost15_128",
            f"{lang}_shuffle_cost15_128",
        ],
        [
            f"{lang}_noshuffle_cost15_4",
            f"{lang}_noshuffle_cost15_4",
            f"{lang}_shuffle_cost15_4",
            f"{lang}_shuffle_cost15_4",
        ],
        [
            f"{lang}_noshuffle_cost15_128",
            f"{lang}_noshuffle_cost15_128",
            f"{lang}_shuffle_cost15_128",
            f"{lang}_shuffle_cost15_128",
        ],
        [
            f"{lang}_noshuffle_cost15_4",
            f"{lang}_noshuffle_cost15_4",
            f"{lang}_shuffle_cost15_4",
            f"{lang}_shuffle_cost15_4",
        ],
    ]

    nrows = len(variants)
    ncols = len(variants[0])

    mechanisms = [["pd", "pi", "pd", "pi"] for _ in range(nrows)]
    if "Imimic" in options["trait"]:
        traits = [[None, options["trait"], None, options["trait"]] for _ in range(nrows)]
    else:
        traits = repeat_for_matrix(options["trait"], nrows, ncols)

    givens_control = [
        [options["given"], options["given"], options["given"], options["given"]],
        [options["given"], options["given"], options["given"], options["given"]],
        ["0.0", "0.0", "0.0", "0.0"],
        ["0.0", "0.0", "0.0", "0.0"],
    ]

    s1 = "$\\mathit{s}_{\\mathit{1}}$"
    s2 = "$\\mathit{s}_{\\mathit{2}}$"
    s3 = "$\\mathit{s}_{\\mathit{3}}$"
    s4 = "$\\mathit{s}_{\\mathit{4}}$"
    s5 = "$\\mathit{s}_{\\mathit{5}}$"

    titles_columns = [
        f"No shuffling\n{s1}, {s4}",
        f"No shuffling\n{s1}, {s2}, {s4}",
        f"Shuffling\n{s1}, {s4}",
        f"Shuffling\n{s1}, {s2}, {s4}",
    ]

    layout = {
        "givens": repeat_for_matrix(options["given"], nrows, ncols),
        "givens_control": givens_control,
        "mechanisms": mechanisms,
        "mechanisms_control": repeat_for_matrix("none", nrows, ncols),
        "titles_columns": titles_columns,
        "titles_rows": [""] * nrows,
        "traits": traits,
        "traits_control": traits,
        "variants": variants,
        "variants_control": variants,
    }

    return layout


def curves(options):
    """Fitness curves for partner choice."""

    givens = [["1.0"], ["0.5"], ["0.0"]]

    nrows = len(givens)

    if "Mimic" in options["trait"]:
        mechanism = "d"
    elif "Choose" in options["trait"]:
        mechanism = "p"
    else:
        mechanism = options["mechanism"]

    traits = repeat_for_matrix(options["trait"], nrows, 1)
    variants = repeat_for_matrix("nolang_noshuffle_cost15_4", nrows, 1)

    layout = {
        "givens": givens,
        "givens_control": givens,
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


def default(options):
    """Four plots."""

    lang = "lang" if options["lang"] else "nolang"

    variants = [
        [f"{lang}_noshuffle_cost15_128", f"{lang}_shuffle_cost15_128"],
        [f"{lang}_noshuffle_cost15_4", f"{lang}_shuffle_cost15_4"],
    ]

    nrows = len(variants)
    ncols = len(variants[0])

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
        "variants": variants,
        "variants_control": variants,
    }

    return layout


def dilemmas(options):
    """Magnitud of social dilemmas."""

    givens = [["1.0", "1.0"], ["0.5", "0.5"]]

    nrows = len(givens)
    ncols = len(givens[0])

    traits = [["qBSeenmean", "wmean"] for _ in range(nrows)]

    layout = {
        "givens": givens,
        "givens_control": repeat_for_matrix("0.0", nrows, ncols),
        "mechanisms": repeat_for_matrix(options["mechanism"], nrows, ncols),
        "mechanisms_control": repeat_for_matrix(
            options["mechanism_control"], nrows, ncols
        ),
        "titles_columns": ["Production of $\\it{B}$", "Fitness"],
        "titles_rows": [""] * nrows,
        "traits": traits,
        "traits_control": traits,
        "variants": repeat_for_matrix("nolang_noshuffle_cost15_4", nrows, ncols),
        "variants_control": repeat_for_matrix(
            "nolang_noshuffle_cost15_4", nrows, ncols
        ),
    }

    return layout


def eight(options):
    """Eight plots. 4 relative to none. 4 relative to social."""

    lang = "lang" if options["lang"] else "nolang"

    variants = [
        [f"{lang}_noshuffle_cost15_128", f"{lang}_shuffle_cost15_128"],
        [f"{lang}_noshuffle_cost15_4", f"{lang}_shuffle_cost15_4"],
        [f"{lang}_noshuffle_cost15_128", f"{lang}_shuffle_cost15_128"],
        [f"{lang}_noshuffle_cost15_4", f"{lang}_shuffle_cost15_4"],
    ]

    nrows = len(variants)
    ncols = len(variants[0])

    givens_control = [
        [options["given"], options["given"]],
        [options["given"], options["given"]],
        ["0.0", "0.0"],
        ["0.0", "0.0"],
    ]

    traits = repeat_for_matrix(options["trait"], nrows, ncols)

    layout = {
        "givens": repeat_for_matrix(options["given"], nrows, ncols),
        "givens_control": givens_control,
        "mechanisms": repeat_for_matrix(options["mechanism"], nrows, ncols),
        "mechanisms_control": repeat_for_matrix(
            options["mechanism_control"], nrows, ncols
        ),
        "titles_columns": ["No shuffling", "Shuffling"],
        "titles_rows": [""] * nrows,
        "traits": traits,
        "traits_control": traits,
        "variants": variants,
        "variants_control": variants,
    }

    return layout


def five(options):
    """1 + 2 + 2 plots."""

    variants = [
        [
            "lang_noshuffle_cost15_128",
            "nolang_shuffle_cost15_128",
            "lang_shuffle_cost15_128",
        ],
        [
            "lang_noshuffle_cost15_4",
            "nolang_shuffle_cost15_4",
            "lang_shuffle_cost15_4",
        ],
    ]

    s1 = "$\\mathit{s}_{\\mathit{1}}$"
    s2 = "$\\mathit{s}_{\\mathit{2}}$"
    s3 = "$\\mathit{s}_{\\mathit{3}}$"

    titles_columns = [
        f"No shuffling\n{s1}, {s3}",
        f"Shuffling\n{s1}, {s2}",
        f"Shuffling\n{s1}, {s2}, {s3}",
    ]

    traits = [
        [options["trait"], None, options["trait"]],
        [options["trait"], None, options["trait"]],
    ]

    nrows = len(variants)
    ncols = len(variants[0])

    layout = {
        "givens": repeat_for_matrix(options["given"], nrows, ncols),
        "givens_control": repeat_for_matrix(options["given_control"], nrows, ncols),
        "mechanisms": repeat_for_matrix(options["mechanism"], nrows, ncols),
        "mechanisms_control": repeat_for_matrix(
            options["mechanism_control"], nrows, ncols
        ),
        "titles_columns": titles_columns,
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
    """Two plots."""

    lang = "lang" if options["lang"] else "nolang"

    variants = [
        [f"{lang}_shuffle_cost15_128"],
        [f"{lang}_shuffle_cost15_4"],
    ]

    nrows = len(variants)
    ncols = len(variants[0])

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
        "variants": variants,
        "variants_control": variants,
    }

    return layout


def ten(options):
    """1 + 2 + 2 plots, twice."""

    variants = [
        [
            "lang_noshuffle_cost15_128",
            "nolang_shuffle_cost15_128",
            "lang_shuffle_cost15_128",
        ],
        [
            "lang_noshuffle_cost15_4",
            "nolang_shuffle_cost15_4",
            "lang_shuffle_cost15_4",
        ],
        [
            "lang_noshuffle_cost15_128",
            "nolang_shuffle_cost15_128",
            "lang_shuffle_cost15_128",
        ],
        [
            "lang_noshuffle_cost15_4",
            "nolang_shuffle_cost15_4",
            "lang_shuffle_cost15_4",
        ],
    ]

    nrows = len(variants)
    ncols = len(variants[0])

    givens = [
        ["1.0", "1.0", "1.0"],
        ["1.0", "1.0", "1.0"],
        ["0.5", "0.5", "0.5"],
        ["0.5", "0.5", "0.5"],
    ]
    
    givens_control = givens
    givens_control = repeat_for_matrix("0.0", nrows, ncols)

    mechanisms = repeat_for_matrix("i", nrows, ncols)

    if options["trait"] == "ImimicGrainmean":
        traits = [[None, options["trait"], options["trait"]] for _ in range(nrows)]
    elif options["trait"] == "Imimic_ltGrainmean":
        traits = [[options["trait"], None, options["trait"]] for _ in range(nrows)]
    else:
        traits = repeat_for_matrix(options["trait"], nrows, ncols)

    s1 = "$\\mathit{s}_{\\mathit{1}}$"
    s2 = "$\\mathit{s}_{\\mathit{2}}$"
    s3 = "$\\mathit{s}_{\\mathit{3}}$"

    titles_columns = [
        f"No shuffling\n{s1}, {s3}",
        f"Shuffling\n{s1}, {s2}",
        f"Shuffling\n{s1}, {s2}, {s3}",
    ]

    layout = {
        "givens": givens,
        "givens_control": givens_control,
        "mechanisms": mechanisms,
        "mechanisms_control": repeat_for_matrix("none", nrows, ncols),
        "titles_columns": titles_columns,
        "titles_rows": [""] * nrows,
        "traits": traits,
        "traits_control": traits,
        "variants": variants,
        "variants_control": variants,
    }

    return layout


def theory(options):
    """First column is theoretical."""

    givens = [[None, "1.0"], [None, "0.5"], [None, "0.0"]]

    nrows = len(givens)

    mechanisms = [[None, "none"] for _ in range(nrows)]
    traits = [[None, options["trait"]] for _ in range(nrows)]
    variants = [[None, "nolang_noshuffle_cost15_4"] for _ in range(nrows)]
    titles_columns = [
        "Production of $\\it{B}$\n(theory)",
        "Production of $\\it{B}$\n(simulations)",
    ]

    layout = {
        "givens": givens,
        "givens_control": repeat_for_matrix(None, nrows, 2),
        "mechanisms": mechanisms,
        "mechanisms_control": mechanisms,
        "titles_columns": titles_columns,
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

    variants = [[f"{lang}_noshuffle_cost15_4"]]

    layout = {
        "givens": [[options["given"]]],
        "givens_control": [[options["given_control"]]],
        "mechanisms": [[options["mechanism"]]],
        "mechanisms_control": [[options["mechanism_control"]]],
        "titles_columns": ["No shuffling"],
        "titles_rows": [""],
        "traits": [[options["trait"]]],
        "traits_control": [[options["trait_control"]]],
        "variants": variants,
        "variants_control": variants,
    }

    return layout
