""" Store the columns and rows for the different modes of the figure """

dict_variant_titles = {
    "nolang_noshuffle": "No shuffling\nShort memory",
    "lang_noshuffle": "No shuffling\nLong memory",
    "nolang_shuffle": "Shuffling\nShort memory",
    "lang_shuffle": "Shuffling\nLong memory",
}

all_variants = ["nolang_noshuffle", "lang_noshuffle", "nolang_shuffle", "lang_shuffle"]

all_lang_variants = ["lang_noshuffle", "lang_shuffle"]

dict_row_titles = {
    "none": "",
    "p": "P",
    "pi": "PR",
    "i": "R",
    "given100": "1",
    "given095": "0.95",
    "given050": "0.5",
    "given000": "0",
}

dict_traits = {
    "ChooseGrain": {
        "mean": "ChooseGrainmean",
        "frq": "ChooseGrain",
        "title": "Partner choice\n(short memory)",
        "relative": "none-",
        "variants": all_variants,
    },
    "Choose_ltGrain": {
        "mean": "Choose_ltGrainmean",
        "frq": "Choose_ltGrain",
        "title": "Partner choice\n(long memory)",
        "relative": "none-",
        "variants": all_lang_variants,
    },
    "MimicGrain": {
        "mean": "MimicGrainmean",
        "frq": "MimicGrain",
        "title": "Direct\nreciprocity",
        "relative": "none-",
        "variants": all_variants,
    },
    "ImimicGrain": {
        "mean": "ImimicGrainmean",
        "frq": "ImimicGrain",
        "title": "Indirect\nreciprocity\n(short memory)",
        "relative": "none-",
        "variants": all_variants,
    },
    "Imimic_ltGrain": {
        "mean": "Imimic_ltGrainmean",
        "frq": "Imimic_ltGrain",
        "title": "Indirect\nreciprocity\n(long memory)",
        "relative": "none-",
        "variants": all_lang_variants,
    },
    "qBSeen": {
        "mean": "qBSeenmean",
        "frq": "qBSeen",
        "title": r"Production of $\it{B}$",
        "relative": "no",
        "variants": all_variants,
    },
    "qBSeen_byproduct": {
        "mean": "qBSeenmean",
        "frq": "qBSeen",
        "title": "Byproduct help",
        "relative": "given",
        "variants": all_variants,
    },
    "qBSeen_excess": {
        "mean": "qBSeenmean",
        "frq": "qBSeen",
        "title": r"Production of $\it{B}$",
        "relative": "-social",
        "variants": all_variants,
    },
    "qBSeen_excess_none": {
        "mean": "qBSeenmean",
        "frq": "qBSeen",
        "title": """Production of $\it{B}$\n(relative)""",
        "relative": "-social",
        "variants": all_variants,
    },
    "w": {
        "mean": "wmean",
        "frq": "w",
        "title": "Fitness",
        "relative": "no",
        "variants": all_variants,
    },
    "w_excess": {
        "mean": "wmean",
        "frq": "w",
        "title": "Fitness",
        "relative": "-social",
        "variants": all_variants,
    },
    "w_excess_none": {
        "mean": "wmean",
        "frq": "w",
        "title": "Fitness\n(relative)",
        "relative": "-social",
        "variants": all_variants,
    },
    "all_traits": {"variants": all_variants},
    "all_lang_traits": {"variants": all_lang_variants},
}

dict_multitrait_rows = {
    "default": ["p", "pi", "i", "none"],
    "none": ["given100", "given095", "given050", "given000"],
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
        "cost15_4",
        "cost15_4",
        "cost15_4",
    ]
}

dict_single_trait_mechanisms = {
    "default": ["p", "pi", "i", "p", "pi", "i"],
}

GIVEN_FOLDER = "given100"
