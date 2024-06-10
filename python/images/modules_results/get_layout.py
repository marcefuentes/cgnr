"""Get data layout for a figure."""


def get_layout(options, layouts):
    """Get data layout for a figure."""

    layout_function = getattr(layouts, options["layout"])
    return layout_function(
        options["trait"],
        options["mechanism"],
        options["given"],
    )
