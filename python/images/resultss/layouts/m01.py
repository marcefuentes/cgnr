"""Single plot."""


def m01(options):
    """Single plot."""

    lang = "lang" if options["lang"] else "nolang"

    variants = [[f"{lang}_noshuffle_cost15_4"]]

    layout = default_layout(variants, options)

    return layout
