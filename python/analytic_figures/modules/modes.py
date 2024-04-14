
""" Store the columns and rows for the different modes of the figure """

from common_modules.get_config import get_config
from modules.get_df import get_df

columns_nolang_lang = [
    "nolang_noshuffle",
    "nolang_shuffle",
    "lang_noshuffle",
    "lang_shuffle"
]

columns_lang = [
    "lang_noshuffle",
    "lang_shuffle"
]

dict_traits = {
    "ChooseGrain": {
        "mean":     "ChooseGrainmean",
        "frq":      "ChooseGrain",
        "title":    "Partner choice\n(short memory)",
        "relative": "none-",
        "columns":  columns_nolang_lang
    },
    "Choose_ltGrain": {
        "mean":     "Choose_ltGrainmean",
        "frq":      "Choose_ltGrain",
        "title":    "Partner choice\n(long memory)",
        "relative": "none-",
        "columns":  columns_lang
    },
    "MimicGrain": {
        "mean":     "MimicGrainmean",
        "frq":      "MimicGrain",
        "title":    "Direct\nreciprocity",
        "relative": "none-",
        "columns":  columns_nolang_lang
    },
    "ImimicGrain": {
        "mean":     "ImimicGrainmean",
        "frq":      "ImimicGrain",
        "title":    "Indirect\nreciprocity\n(short memory)",
        "relative": "none-",
        "columns":  columns_nolang_lang
    },
    "Imimic_ltGrain": {
        "mean":     "Imimic_ltGrainmean",
        "frq":      "Imimic_ltGrain",
        "title":    "Indirect\nreciprocity\n(long memory)",
        "relative": "none-",
        "columns":  columns_lang
    },
    "qBSeen": {
        "mean":     "qBSeenmean",
        "frq":      "qBSeen",
        "title":    r"Production of $\it{B}$",
        "relative": "no",
        "columns":  columns_nolang_lang
    },
    "qBSeen_byproduct": {
        "mean":     "qBSeenmean",
        "frq":      "qBSeen",
        "title":    "Byproduct help",
        "relative": "given",
        "columns":  columns_nolang_lang
    },
    "qBSeen_excess": {
        "mean":     "qBSeenmean",
        "frq":      "qBSeen",
        "title":    r"Production of $\it{B}$",
        "relative": "-social",
        "columns":  columns_nolang_lang
    },
    "w": {
        "mean":     "wmean",
        "frq":      "w",
        "title":    "Fitness",
        "relative": "no",
        "columns":  columns_nolang_lang
    },
    "w_excess": {
        "mean":     "wmean",
        "frq":      "w",
        "title":    "Fitness",
        "relative": "-social",
        "columns":  columns_nolang_lang
    },
    "all_lang": {
        "columns":  columns_lang
    },
    "all": {
        "columns":  columns_nolang_lang
    }
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
    ]
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
    ]
}

rows_trait = [
    "cost15_128",
    "cost15_128",
    "cost15_128",
    "cost15_4",
    "cost15_4",
    "cost15_4"
]

mechanisms_trait = [
   "p",
   "pi",
   "i",
   "p",
   "pi",
    "i"
]

GIVEN_FOLDER = "given100"

def look_in(dictionary, key, field):
    """ Return a value from a dictionary """

    if key in dictionary:
        return dictionary[key][field]
    return ""

def get_columns(key):
    """ Return the columns for the key """
    if key in dict_traits:
        return dict_traits[key]["columns"]
    try:
        return dict_columns[key]
    except KeyError as exc:
        raise ValueError(f"{key} not found") from exc

def get_rows(key):
    """ Return the rows for the keye """

    if key in dict_traits:
        return rows_trait
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
            path = f"none/{GIVEN_FOLDER}"
        else:
            path = f"{row}/{GIVEN_FOLDER}"
        dfs.append(get_df(path, csv0, movie))
        if histogram:
            dffrqs.append(get_df(path, csv1, movie))
    if "none" in rows:
        df_none = dfs[rows.index("none")]
    else:
        path = f"none/{GIVEN_FOLDER}"
        df_none = get_df(path, csv0, movie)
    if "social" in rows:
        df_social = dfs[rows.index("social")]
    else:
        path = "none/given000"
        df_social = get_df(path, csv0, movie)
    return dfs, df_none, df_social, dffrqs

def get_data_trait(mode, histogram, movie):
    """ Get the data. """

    columns_trait = get_columns(mode)
    nrows = len(rows_trait)
    ncolumns = len(columns_trait)

    dfs =           [[None for _ in range(ncolumns)] for _ in range(nrows)]
    df_nones =      [[None for _ in range(ncolumns)] for _ in range(nrows)]
    df_socials =    [[None for _ in range(ncolumns)] for _ in range(nrows)]
    if histogram:
        dffrqs =    [[None for _ in range(len(ncolumns))] for _ in range(nrows)]
    else:
        dffrqs =    []
    csv0, csv1 = get_config("output_file_extensions")
    for r, row, mechanism in zip(range(nrows), rows_trait, mechanisms_trait):
        for c, column in enumerate(columns_trait):
            path = f"{column}_{row}/{mechanism}/{GIVEN_FOLDER}"
            if histogram:
                dffrqs[r][c] =  get_df(path, csv1, movie)
            dfs[r][c] =         get_df(path, csv0, movie)
            df_nones[r][c] =    get_df(f"{column}_{row}/none/{GIVEN_FOLDER}", csv0, movie)
            df_socials[r][c] =  get_df(f"{column}_{row}/none/given000", csv0, movie)
    return dfs, df_nones, df_socials, dffrqs
