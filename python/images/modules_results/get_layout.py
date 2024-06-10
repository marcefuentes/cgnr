"""Get data layout for a figure."""

import settings_results.layouts as layouts


def get_layout(options):
    """Get data layout for a figure."""

    figure = options["figure"]
    trait = options["trait"]
    mechanism = options["mechanism"]
    given = options["given"]

    if figure == "figure_2":
        return layouts.figure_2(trait)
    elif figure == "figure_3":
        return layouts.figure_3(trait, mechanism, given)
    elif figure == "curves":
        return layouts.curves(trait)
    else:
        raise ValueError(f"Unknown figure: {figure}")
