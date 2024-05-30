"""Layouts for single folder plots."""

columns = {
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


rows = {
    "default": ["p", "pi", "i", "none"],
    "none": ["1.0", "0.0"],
    "test": ["p", "i", "none"],
}
