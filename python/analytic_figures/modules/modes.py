
""" Store the columns and rows for the different modes of the figure """

from common_modules.get_config import get_config
from modules.get_df import get_df

dict_variants_all = {
    "nolang_noshuffle": {
        "title":    "Short memory\nNo shuffle"
    },
    "nolang_shuffle": {
        "title":    "Short memory\nShuffle"
    },
    "lang_noshuffle": {
        "title":    "Long memory\nNo shuffle"
    },
    "lang_shuffle": {
        "title":    "Long memory\nShuffle"
    }
}

dict_variants_lang = {
    "lang_noshuffle": {
        "title":    "Long memory\nNo shuffle"
    },
    "lang_shuffle": {
        "title":    "Long memory\nShuffle"
    }
}

dict_traits = {
    "ChooseGrain": {
        "mean":     "ChooseGrainmean",
        "frq":      "ChooseGrain",
        "title":    "Partner choice\n(short memory)",
        "relative": "none-",
        "columns":  dict_variants_all
    },
    "Choose_ltGrain": {
        "mean":     "Choose_ltGrainmean",
        "frq":      "Choose_ltGrain",
        "title":    "Partner choice\n(long memory)",
        "relative": "none-",
        "columns":  dict_variants_lang
    },
    "MimicGrain": {
        "mean":     "MimicGrainmean",
        "frq":      "MimicGrain",
        "title":    "Direct\nreciprocity",
        "relative": "none-",
        "columns":  dict_variants_all
    },
    "ImimicGrain": {
        "mean":     "ImimicGrainmean",
        "frq":      "ImimicGrain",
        "title":    "Indirect\nreciprocity\n(short memory)",
        "relative": "none-",
        "columns":  dict_variants_all
    },
    "Imimic_ltGrain": {
        "mean":     "Imimic_ltGrainmean",
        "frq":      "Imimic_ltGrain",
        "title":    "Indirect\nreciprocity\n(long memory)",
        "relative": "none-",
        "columns":  dict_variants_lang
    },
    "qBSeen": {
        "mean":     "qBSeenmean",
        "frq":      "qBSeen",
        "title":    r"Production of $\it{B}$",
        "relative": "no",
        "columns":  dict_variants_all
    },
    "qBSeen_byproduct": {
        "mean":     "qBSeenmean",
        "frq":      "qBSeen",
        "title":    "Byproduct help",
        "relative": "given",
        "columns":  dict_variants_all
    },
    "qBSeen_excess": {
        "mean":     "qBSeenmean",
        "frq":      "qBSeen",
        "title":    r"Production of $\it{B}$",
        "relative": "-social",
        "columns":  dict_variants_all
    },
    "w": {
        "mean":     "wmean",
        "frq":      "w",
        "title":    "Fitness",
        "relative": "no",
        "columns":  dict_variants_all
    },
    "w_excess": {
        "mean":     "wmean",
        "frq":      "w",
        "title":    "Fitness",
        "relative": "-social",
        "columns":  dict_variants_all
    },
    "all_lang": {
        "columns":  dict_variants_lang
    },
    "all": {
        "columns":  dict_variants_all
    }
}

dict_multitrait_rows = {
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

dict_multitrait_modes = {
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

list_rows_single_trait = [
    "cost15_128",
    "cost15_128",
    "cost15_128",
    "cost15_4",
    "cost15_4",
    "cost15_4"
]

list_mechanisms_single_trait = [
   "p",
   "pi",
   "i",
   "p",
   "pi",
    "i"
]

GIVEN_FOLDER = "given100"

def get_data_multitrait(mode, histogram, movie):
    """ Get the data. """

    dfs = []
    dffrqs = []

    if mode in dict_multitrait_rows:
        rows = dict_multitrait_rows[mode]
    else:
        rows = dict_multitrait_rows["default"]

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

def get_data_single_trait(trait, histogram, movie):
    """ Get the data. """

    columns = dict_traits[trait]["columns"]
    rows = list_rows_single_trait
    mechanisms = list_mechanisms_single_trait
    nrows = len(rows)
    ncolumns = len(columns)

    dfs =           [[None for _ in range(ncolumns)] for _ in range(nrows)]
    df_nones =      [[None for _ in range(ncolumns)] for _ in range(nrows)]
    df_socials =    [[None for _ in range(ncolumns)] for _ in range(nrows)]
    if histogram:
        dffrqs =    [[None for _ in range(ncolumns)] for _ in range(nrows)]
    else:
        dffrqs =    []
    csv0, csv1 = get_config("output_file_extensions")
    for r, row, mechanism in zip(range(nrows), rows, mechanisms):
        for c, column in enumerate(columns):
            path = f"{column}_{row}/{mechanism}/{GIVEN_FOLDER}"
            if histogram:
                dffrqs[r][c] =  get_df(path, csv1, movie)
            dfs[r][c] =         get_df(path, csv0, movie)
            df_nones[r][c] =    get_df(f"{column}_{row}/none/{GIVEN_FOLDER}", csv0, movie)
            df_socials[r][c] =  get_df(f"{column}_{row}/none/given000", csv0, movie)
    return dfs, df_nones, df_socials, dffrqs
