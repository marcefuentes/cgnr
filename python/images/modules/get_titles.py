""" Creates list of titles """

from modules.titles import TITLES


def get_titles(keys):
    """Reads the titles file and returns the value of the variable passed as argument"""

    titles = []
    for key in keys:
        if not key:
            titles.append("")
            continue
        #title = TITLES[key].replace("\\n", "\n")
        title = TITLES[key]
        titles.append(title)

    return titles
