"""Theory and simulations."""

from resultsm.repeat_for_matrix import repeat_for_matrix


def theory(options):
    """First column is theoretical."""

    givens = [[None, "1.0"], [None, "0.5"], [None, "0.0"]]

    nrows = len(givens)

    mechanisms = [[None, "none"] for _ in range(nrows)]
    traits = [[None, options["traits"]] for _ in range(nrows)]
    variants = [[None, "nolang_noshuffle_cost15_4"] for _ in range(nrows)]
    titles_columns = [
        "Production of $\\it{B}$\n(theory)",
        "Production of $\\it{B}$\n(simulations)",
    ]

    options = {
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

    return options
