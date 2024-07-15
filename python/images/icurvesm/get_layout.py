"""Get data layout for a figure."""

from icurvess import layouts


def get_layout(options):
    """Get data layout for a figure."""

    layout_function = getattr(layouts, options["layout"])
    return layout_function(options)
