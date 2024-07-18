"""Default data."""

from .repeat_for_matrix import repeat_for_matrix
from .ss import S1, S2, S3, S4, S5


def default_data(data, variants):
    """Default data."""

    nrows = len(variants)
    ncols = len(variants[0])

    data["givens"] = repeat_for_matrix(data["givens"], nrows, ncols)
    data["givens_control"] = repeat_for_matrix(data["givens_control"], nrows, ncols)
    data["mechanisms"] = repeat_for_matrix(data["mechanisms"], nrows, ncols)
    data["mechanisms_control"] = repeat_for_matrix(
        data["mechanisms_control"], nrows, ncols
    )
    data["titles_rows"] = [""] * nrows
    data["traits"] = repeat_for_matrix(data["traits"], nrows, ncols)
    data["traits_control"] = repeat_for_matrix(data["traits_control"], nrows, ncols)
    data["variants"] = variants
    data["variants_control"] = variants

    return data


def default_data_ipi(data, mechanisms, variants_common):
    """Default data for large figures with subtitles."""

    suffixes = ["_128", "_4"]
    variants = []
    for _ in range(2):
        for suffix in suffixes:
            variants.append([f"{variant}{suffix}" for variant in variants_common])

    nrows = len(variants)
    ncols = len(variants_common)

    givens, givens_control = get_givens(data["givens_control"], nrows, ncols)
    data = default_data(data, variants)

    data["givens"] = givens
    data["givens_control"] = givens_control
    data["mechanisms"] = [mechanisms for _ in range(nrows)]
    data["titles_columns"] = get_titles(variants_common)

    return data


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


def get_givens(control, nrows, ncols):
    """Get givens."""

    givens = [
        ["1.0" for _ in range(ncols)],
        ["1.0" for _ in range(ncols)],
        ["0.5" for _ in range(ncols)],
        ["0.5" for _ in range(ncols)],
    ]

    if control == "0.0":
        givens_control = repeat_for_matrix("0.0", nrows, ncols)
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
