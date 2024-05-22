""" Store the columns and rows for the different trait_sets of the figure """

variants = ["nolang_noshuffle", "lang_noshuffle", "nolang_shuffle", "lang_shuffle"]

dict_single_trait_variant_suffixes = {
    "default": [
        "cost15_128",
        "cost15_128",
        "cost15_128",
        "cost15_128",
        "cost15_128",
        "cost15_4",
        "cost15_4",
        "cost15_4",
        "cost15_4",
        "cost15_4",
    ]
}

dict_single_trait_mechanisms = {
    "default": ["p", "pd", "d", "pi", "i", "p", "pd", "d", "pi", "i"],
}

GIVEN_FOLDER = "1"

all_traits = [
    "ChooseGrain",
    "Choose_ltGrain",
    "MimicGrain",
    "ImimicGrain",
    "Imimic_ltGrain",
    "w_excess",
    "qBSeen_excess",
]

dict_traits = {
    "ChooseGrain": {
        "mean": "ChooseGrainmean",
        "frq": "ChooseGrain",
        "relative": "none-",
    },
    "Choose_ltGrain": {
        "mean": "Choose_ltGrainmean",
        "frq": "Choose_ltGrain",
        "relative": "none-",
    },
    "MimicGrain": {
        "mean": "MimicGrainmean",
        "frq": "MimicGrain",
        "relative": "none-",
    },
    "ImimicGrain": {
        "mean": "ImimicGrainmean",
        "frq": "ImimicGrain",
        "relative": "none-",
    },
    "Imimic_ltGrain": {
        "mean": "Imimic_ltGrainmean",
        "frq": "Imimic_ltGrain",
        "relative": "none-",
    },
    "qBSeen": {
        "mean": "qBSeenmean",
        "frq": "qBSeen",
        "relative": "no",
    },
    "qBSeen_byproduct": {
        "mean": "qBSeenmean",
        "frq": "qBSeen",
        "relative": "given",
    },
    "qBSeen_excess": {
        "mean": "qBSeenmean",
        "frq": "qBSeen",
        "relative": "-social",
    },
    "qBSeen_excess_none": {
        "mean": "qBSeenmean",
        "frq": "qBSeen",
        "relative": "-social",
    },
    "w": {
        "mean": "wmean",
        "frq": "w",
        "relative": "no",
    },
    "w_excess": {
        "mean": "wmean",
        "frq": "w",
        "relative": "-social",
    },
    "w_excess_none": {
        "mean": "wmean",
        "frq": "w",
        "relative": "-social",
    },
    "all_traits": {},
}

dict_single_folder_rows = {
    "default": ["p", "pi", "i", "none"],
    "none": ["1", "0"],
    "test": ["p", "i", "none"],
}

dict_single_folder_columns = {
    "cooperation": [
        "ChooseGrain",
        "MimicGrain",
        "ImimicGrain",
        "qBSeen_excess",
        "w_excess",
    ],
    "cooperationlt": [
        "ChooseGrain",
        "Choose_ltGrain",
        "MimicGrain",
        "ImimicGrain",
        "Imimic_ltGrain",
        "qBSeen_excess",
        "w_excess",
    ],
    "correlationsqB": ["r_qB_Choose", "r_qB_Mimic", "r_qB_Imimic"],
    "correlationsqBlt": [
        "r_qB_Choose",
        "r_qB_Choose_lt",
        "r_qB_Mimic",
        "r_qB_Imimic",
        "r_qB_Imimic_lt",
    ],
    "correlations": ["r_Choose_Mimic", "r_Choose_Imimic", "r_Mimic_Imimic"],
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
        "r_Imimic_Imimic_lt",
    ],
    "none": ["qBSeen", "qBSeen_excess_none", "w", "w_excess_none"],
    "test": ["qBSeen", "w"],
}
