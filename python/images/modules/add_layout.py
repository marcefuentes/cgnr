"""Get data layout for a figure."""


def add_layout(data, layouts):
    """Get data layout for a figure."""

    layout_function = getattr(layouts, data["layout"])
    layout_function(data)
