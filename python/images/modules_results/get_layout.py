"""Get data layout for a figure."""

import settings_results.layouts as layouts


def get_layout(options):
    """Get data layout for a figure."""

    layout_function = getattr(layouts, options["figure"])
    return layout_function(
        options["trait"],
        options["mechanism"],
        options["given"],
    )
