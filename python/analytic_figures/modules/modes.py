
""" Store the columns and rows for the different modes of the figure """

from common_modules.get_config import get_config
from modules.get_df import get_df

dict_traits = {
    "ChooseGrain": {
        "mean":     "ChooseGrainmean",
        "frq":      "ChooseGrain",
        "title":    "Partner choice\n(short memory)",
        "relative": "none-"
    },
    "Choose_ltGrain": {
        "mean":     "Choose_ltGrainmean",
        "frq":      "Choose_ltGrain",
        "title":    "Partner choice\n(long memory)",
        "relative": "none-"
    },
    "MimicGrain": {
        "mean":     "MimicGrainmean",
        "frq":      "MimicGrain",
        "title":    "Direct\nreciprocity",
        "relative": "none-"
    },
    "ImimicGrain": {
        "mean":     "ImimicGrainmean",
        "frq":      "ImimicGrain",
        "title":    "Indirect\nreciprocity\n(short memory)",
        "relative": "none-"
    },
    "Imimic_ltGrain": {
        "mean":     "Imimic_ltGrainmean",
        "frq":      "Imimic_ltGrain",
        "title":    "Indirect\nreciprocity\n(long memory)",
        "relative": "none-"
    },
    "qBSeen": {
        "mean":     "qBSeenmean",
        "frq":      "qBSeen",
        "title":    "Production of $\it{B}$",
        "relative": "no"
    },
    "qBSeen_byproduct": {
        "mean":     "qBSeenmean",
        "frq":      "qBSeen",
        "title":    "Byproduct help",
        "relative": "given"
    },
    "qBSeen_excess": {
        "mean":     "qBSeenmean",
        "frq":      "qBSeen",
        "title":    "Production of $\it{B}$",
        "relative": "-social"
    },
    "w": {
        "mean":     "wmean",
        "frq":      "w",
        "title":    "Fitness",
        "relative": "no"
    },
    "w_excess": {
        "mean":     "wmean",
        "frq":      "w",
        "title":    "Fitness",
        "relative": "-social"
    }
}

dict_columns = {
    "cooperation": [
        "ChooseGrain",
        "MimicGrain",
        "ImimicGrain",
        "qBSeen_excess",
        "w_excess"
    ],
    "cooperationlt": [
        "ChooseGrain",
        "Choose_ltGrain",
        "MimicGrain",
        "ImimicGrain",
        "Imimic_ltGrain",
        "qBSeen_excess",
        "w_excess"
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
        "w_excess"
    ],
    "test": [
        "qBSeen",
        "w"
    ],
    "trait": [
        "nolang",
        "lang",
        "nolang",
        "lang"
    ],
}

dict_rows = {
    "default": [
        "pi",
        "p",
        "i",
        "none"
    ],
    "none": [
        "given100",
        "given095",
        "given050",
        "given000"
    ],
    "test": [
        "p",
        "i",
        "none"
    ],
    "trait": [
        "noshuffle",
        "shuffle",
        "noshuffle",
        "shuffle"
    ],
}

given_folder = "given100"

def look_in(dictionary, key, field):
    """ Return a value from a dictionary """

    if key in dictionary:
        return dictionary[key][field]
    return ""

def get_columns(key):
    """ Return the columns for the key """

    if key in dict_traits:
        return dict_columns["trait"]
    try:
        return dict_columns[key]
    except KeyError as exc:
        raise ValueError(f"{mode} not found") from exc

def get_rows(key):
    """ Return the rows for the keye """

    if key in dict_traits:
        return dict_rows["trait"]
    if key in dict_rows:
        return dict_rows[key]
    return dict_rows["default"]

def get_data_variant(mode, histogram, movie):
    """ Get the data. """

    dfs = []
    dffrqs = []

    rows = get_rows(mode)

    csv0, csv1 = get_config("output_file_extensions")
    for row in rows:
        if row == "social":
            path = "none/given000"
        elif "none" in row:
            path = f"none/{given_folder}"
        else:
            path = f"{row}/{given_folder}"
        dfs.append(get_df(path, csv0, movie))
        if histogram:
            dffrqs.append(get_df(path, csv1, movie))
    if "none" in rows:
        df_none = dfs[rows.index("none")]
    else:
        path = f"none/{given_folder}"
        df_none = get_df(path, csv0, movie)
    if "social" in rows:
        df_social = dfs[rows.index("social")]
    else:
        path = "none/given000"
        df_social = get_df(path, csv0, movie)
    return dfs, df_none, df_social, dffrqs

def get_data_trait(mode, histogram, movie):
    """ Get the data. """

    rows = get_rows(mode)
    columns = get_columns(mode)

    dfs =           [[None for _ in range(len(columns))] for _ in range(len(rows))]
    df_nones =      [[None for _ in range(len(columns))] for _ in range(len(rows))]
    df_socials =    [[None for _ in range(len(columns))] for _ in range(len(rows))]
    if histogram:
        dffrqs =    [[None for _ in range(len(columns))] for _ in range(len(rows))]
    else:
        dffrqs =    []
    csv0, csv1 = get_config("output_file_extensions")
    for r, row in enumerate(rows):
        for c, column in enumerate(columns):
            folder = f"{column}_{row}_cost{cost}_{groupsize}"
            path = f"{folder}/{mode}/{given_folder}"
            if histogram:
                dffrqs[c][r] =  get_df(path, csv1, movie)
            dfs[c][r] =         get_df(path, csv0, movie)
            df_nones[c][r] =    get_df(f"{folder}/none/{given_folder}", csv0, movie)
            df_socials[c][r] =  get_df(f"{folder}/none/given000", csv0, movie)
    return dfs, df_nones, df_socials, dffrqs
