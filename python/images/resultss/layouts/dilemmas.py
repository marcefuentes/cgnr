"""Social dilemmas."""

from resultsm.repeat_for_matrix import repeat_for_matrix


def dilemmas(options):
    """Magnitude of social dilemmas."""

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
