"""5 plots."""

from .m10 import m10


def m05(data):
    """1 + 2 + 2 plots."""

    data_m10 = m10(data)

    data["givens"] = data_m10["givens"][:-2]
    data["givens_control"] = data_m10["givens_control"][:-2]
    data["mechanisms"] = data_m10["mechanisms"][:-2]
    data["mechanisms_control"] = data_m10["mechanisms_control"][:-2]
    data["titles_columns"] = data_m10["titles_columns"]
    data["titles_rows"] = data_m10["titles_rows"][:-2]
    data["traits"] = data_m10["traits"][:-2]
    data["traits_control"] = data_m10["traits_control"][:-2]
    data["variants"] = data_m10["variants"][:-2]
    data["variants_control"] = data_m10["variants_control"][:-2]

    return data
