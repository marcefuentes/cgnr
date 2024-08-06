"""Add content to data and image dictionaries."""


def add_data(data, image):
    """Add data to dictionary data"""

    data["color_map"] = image["color_map"]
    image["nr"] = data["layout_k"] = len(data["alphas"])
    image["nc"] = data["layout_m"] = len(data["rhos"])
    image["fig_layout"] = {
        "nc": (1 if data["ax_type"] == "AxesImage" else image["nc"]),
        "ncols": data["layout_j"],
        "nr": (1 if data["ax_type"] == "AxesImage" else image["nr"]),
        "nrows": data["layout_i"],
    }
    image["letters"]["y"] = 1.0 + image["padding_letter"] * image["fig_layout"]["nr"]
    image["titles_columns"] = data["titles_columns"]
    image["titles_rows"] = data["titles_rows"]
    image["ticklabels_x"] = [
        f"{data["rhos"][0]:.0f}",
        f"{data["rhos"][len(data['rhos']) // 2]:.0f}",
        f"{data["rhos"][-1]:.2f}",
    ]
    image["ticklabels_y"] = [
        f"{data["alphas"][0]:.1f}",
        f"{data["alphas"][len(data['alphas']) // 2]:.1f}",
        f"{data["alphas"][-1]:.1f}",
    ]
