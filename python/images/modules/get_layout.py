"""Get data layout for a figure."""


def get_layout(data, layouts):
    """Get data layout for a figure."""

    layout_function = getattr(layouts, data["layout"])
    layout_function(data)
