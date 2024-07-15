"""Single plot."""


def m01(options):
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
