""" Store the columns and rows for the different modes of the figure """

all_variants = ["nolang_noshuffle", "lang_noshuffle", "nolang_shuffle", "lang_shuffle"]

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
        "variants": all_variants,
    },
    "Choose_ltGrain": {
        "mean": "Choose_ltGrainmean",
        "frq": "Choose_ltGrain",
        "relative": "none-",
        "variants": all_variants,
    },
    "MimicGrain": {
        "mean": "MimicGrainmean",
        "frq": "MimicGrain",
        "relative": "none-",
        "variants": all_variants,
    },
    "ImimicGrain": {
        "mean": "ImimicGrainmean",
        "frq": "ImimicGrain",
        "relative": "none-",
        "variants": all_variants,
    },
    "Imimic_ltGrain": {
        "mean": "Imimic_ltGrainmean",
        "frq": "Imimic_ltGrain",
        "relative": "none-",
        "variants": all_variants,
    },
    "qBSeen": {
        "mean": "qBSeenmean",
        "frq": "qBSeen",
        "relative": "no",
        "variants": all_variants,
    },
    "qBSeen_byproduct": {
        "mean": "qBSeenmean",
        "frq": "qBSeen",
        "relative": "given",
        "variants": all_variants,
    },
    "qBSeen_excess": {
        "mean": "qBSeenmean",
        "frq": "qBSeen",
        "relative": "-social",
        "variants": all_variants,
    },
    "qBSeen_excess_none": {
        "mean": "qBSeenmean",
        "frq": "qBSeen",
        "relative": "-social",
        "variants": all_variants,
    },
    "w": {
        "mean": "wmean",
        "frq": "w",
        "relative": "no",
        "variants": all_variants,
    },
    "w_excess": {
        "mean": "wmean",
        "frq": "w",
        "relative": "-social",
        "variants": all_variants,
    },
    "w_excess_none": {
        "mean": "wmean",
        "frq": "w",
        "relative": "-social",
        "variants": all_variants,
    },
    "all_traits": {"variants": all_variants},
}

dict_multitrait_rows = {
    "default": ["p", "pi", "i", "none"],
    "none": ["given100", "given000"],
    "test": ["p", "i", "none"],
}

dict_multitrait_columns = {
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
    "none": ["qBSeen", "qBSeen_excess_none", "qBSeen_byproduct", "w", "w_excess_none"],
    "test": ["qBSeen", "w"],
}

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

GIVEN_FOLDER = "given100"
