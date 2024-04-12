
""" Store the columns and rows for the different modes of the figure """

from common_modules.get_config import get_config
from modules.get_df import get_df

title = {
    "ChooseGrain":          "Partner choice\n(short memory)",
    "Choose_ltGrain":       "Partner choice\n(long memory)",
    "MimicGrain":           "Direct\nreciprocity",
    "ImimicGrain":          "Indirect\nreciprocity\n(short memory)",
    "Imimic_ltGrain":       "Indirect\nreciprocity\n(long memory)",
    "qBSeen":               r"Production of $\it{B}$",
    "qBSeen_byproduct":     "Byproduct help",
    "w":                    "Fitness",
    "w_deficit":            "Fitness deficit",
}

columns = {
    "cooperation": [
        "ChooseGrain",
        "MimicGrain",
        "ImimicGrain",
        "qBSeen",
        "w"
    ],
    "cooperationlt": [
        "ChooseGrain",
        "Choose_ltGrain",
        "MimicGrain",
        "ImimicGrain",
        "Imimic_ltGrain",
        "qBSeen",
        "w"
    ],
    "correlationsqB": [
        "r_qB_Choose",
        "r_qB_Mimic",
        "r_qB_Imimic"
    ],
    "correlationsqBlt": [
        "r_qB_Choose",
        "r_qB_Choose_lt",
        "r_qB_Mimic",
        "r_qB_Imimic",
        "r_qB_Imimic_lt"
    ],
    "correlations": [
        "r_Choose_Mimic",
        "r_Choose_Imimic",
        "r_Mimic_Imimic"
    ],
    "correlationsmlt": [
        "r_Choose_Choose_lt",
        "r_Choose_Mimic",
        "r_Choose_Imimic",
        "r_Choose_Imimic_lt",
        "r_Choose_lt_Mimic",
        "r_Choose_lt_Imimic",
        "r_Choose_lt_Imimic_lt",
        "r_Mimic_Imimic",
        "r_Mimic_Imimic_lt",
        "r_Imimic_Imimic_lt"
    ],
    "none": [
        "qBSeen",
        "qBSeen_byproduct",
        "w",
        "w_deficit"
    ],
    "test": [
        "qBSeen",
        "w"
    ],
    "p": [
        "nolang",
        "lang"
    ],
    "r": [
        "nolang",
        "lang"
    ],
    "i": [
        "nolang",
        "lang"
    ],
}

rows = {
    "default":  ["pi", "p", "i", "none"],
    "none":     ["given100", "given095", "given050", "given000"],
    "test":     ["p", "i", "none"],
    "p":        ["no_shuffle", "shuffle"],
    "r":        ["no_shuffle", "shuffle"],
    "i":        ["no_shuffle", "shuffle"]
}

traits = {
    "p": "ChooseGrain",
    "r": "MimicGrain",
    "i": "ImimicGrain",
}

given = "given100"

def get_title(trait):
    """ Return the title of the trait """
    try:
        return title[trait]
    except KeyError:
        return trait

def get_columns(mode):
    """ Return the columns for the mode """
    try:
        return columns[mode]
    except KeyError as exc:
        raise ValueError(f"{mode} not found") from exc

def get_rows(mode):
    """ Return the rows for the mode """
    try:
        return rows[mode]
    except KeyError:
        return rows["default"]

def get_trait(mode):
    """ Return the trait for the mode """
    try:
        return traits[mode]
    except KeyError:
        return mode

def get_data_mechanisms(mode, histogram, movie):
    """ Get the data. """

    dfs = []
    dffrqs = []

    rows = get_rows(mode)

    csv0, csv1 = get_config("output_file_extensions")
    for row in rows:
        if row == "social":
            path = "none/given000"
        elif "none" in row:
            path = f"none/{given}"
        else:
            path = f"{row}/{given}"
        dfs.append(get_df(path, csv0, movie))
        if histogram:
            dffrqs.append(get_df(path, csv1, movie))
    if "none" in rows:
        df_none = dfs[rows.index("none")]
    else:
        path = "none/given100"
        df_none = get_df(path, csv0, movie)
    if "social" in rows:
        df_social = dfs[rows.index("social")]
    else:
        path = "none/given000"
        df_social = get_df(path, csv0, movie)
    return dfs, df_none, df_social, dffrqs

