""" Data layout. """


def figure_2(trait):
    """Figure 2."""

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
        "variants": [[variant for _ in nrange(ncols)] for _ in range(nrows)],
        "variants_control": [[variant for _ in range(ncols)] for _ in range(nrows)],
        "row_titles": ["", ""],
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


def curves(trait):
    """Fitness curves for partner choice."""

    given_list = [["0.5", "1.0"]]

    variant = "nolang_noshuffle_cost15_4"

    if trait == "MimicGrain":
        mechanism = "d"
    elif trait == "ChooseGrain":
        mechanism = "p"

    layout = {
        "column_titles": ["0.5", "1.0"],
        "givens": given_list,
        "givens_control": given_list,
        "mechanisms": [[mechanism, mechanism]],
        "mechanisms_control": [["none", "none"]],
        "variants": [[variant, variant]],
        "variants_control": [[variant, variant]],
        "row_titles": [""],
        "traits": [[trait, trait]],
    }

    return layout


def get_data_layout(figure, trait, mechanism, given):
    """Get data layout for a figure."""

    if figure == "figure_2":
        return figure_2(trait)
    elif figure == "figure_3":
        return figure_3(trait, mechanism, given)
    elif figure == "curves":
        return curves(trait)
    else:
        raise ValueError(f"Unknown figure: {figure}")
