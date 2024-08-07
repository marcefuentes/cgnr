"""Default data."""

from modules.fill_matrix import fill_matrix
from resultss.ss import S1, S2, S3, S4, S5


def add_default_data(data, variants):
    """Default data."""

    data["givens"] = fill_matrix(data["givens"], variants)
    data["givens_control"] = fill_matrix(data["givens_control"], variants)
    data["layout_i"] = len(variants)
    data["layout_j"] = len(variants[0])
    data["mechanisms"] = fill_matrix(data["mechanisms"], variants)
    data["mechanisms_control"] = fill_matrix(data["mechanisms_control"], variants)
    data["titles_columns"] = [""] * len(variants[0])
    data["titles_rows"] = [""] * len(variants)
    data["traits"] = fill_matrix(data["traits"], variants)
    data["traits_control"] = fill_matrix(data["traits_control"], variants)
    data["variants"] = variants
    data["variants_control"] = variants


def add_default_data_ipi(data, mechanisms, variants_common):
    """Default data for large figures with subtitles."""

    suffixes = ["_128", "_4"]
    variants = []
    for _ in range(2):
        for suffix in suffixes:
            variants.append([f"{variant}{suffix}" for variant in variants_common])

    givens, givens_control = get_givens(data["givens_control"], variants)
    add_default_data(data, variants)

    data["givens"] = givens
    data["givens_control"] = givens_control
    data["layout_i"] = len(variants)
    data["layout_j"] = len(variants[0])
    data["mechanisms"] = [mechanisms for _ in variants]
    data["titles_columns"] = get_titles(variants_common)


def get_givens(control, variants):
    """Get givens."""

    givens = [
        ["1.0" for _ in variants[0]],
        ["1.0" for _ in variants[0]],
        ["0.5" for _ in variants[0]],
        ["0.5" for _ in variants[0]],
    ]

    if control == "0.0":
        givens_control = fill_matrix("0.0", variants)
    else:
        givens_control = givens

    return givens, givens_control


def get_subtitles(titles, variants, mechanisms):
    """Get subtitles."""

    for column, (variant, mechanism) in enumerate(zip(variants, mechanisms)):
        if "d" in mechanism:
            titles[column] += f"\n{S1}"
        if "i" in mechanism:
            titles[column] += f"\n{S1}"
            if "nolang" in variant:
                titles[column] += f", {S2}"
            else:
                if "_shuffle" in variant or "p" in mechanism:
                    titles[column] += f", {S2}"
                titles[column] += f", {S3}"
        if mechanism == "p":
            titles[column] += f"\n{S4}"
            if variant.startswith("lang"):
                titles[column] += f"\n{S5}"
        if mechanism in ("pd", "pi"):
            titles[column] += f", {S4}"
            if variant.startswith("lang"):
                titles[column] += f", {S5}"

    return titles


def get_titles(variants):
    """Get titles."""

    titles = []
    for variant in variants:
        if not variant:
            titles.append("")
        elif "noshuffle" in variant:
            titles.append("No shuffling")
        else:
            titles.append("Shuffling")
    return titles
