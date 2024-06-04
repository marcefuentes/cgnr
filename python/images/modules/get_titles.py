""" Creates list of titles """


def get_titles(add_titles, keys, titles_dict):
    """Reads the titles file and returns the value of the variable passed as argument"""

    titles = []
    for key in keys:
        if not key or key not in titles_dict or not add_titles:
            titles.append("")
            continue
        # title = titles_dict[key].replace("\\n", "\n")
        title = titles_dict[key]
        titles.append(title)

    return titles
