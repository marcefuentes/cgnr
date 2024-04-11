
""" Store the traits and rows for the different modes of the figure """

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

traits = {
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
    ]
}

mechanisms = {
    "default":  ["pi", "p", "i", "none"],
    "none":     ["given100", "given095", "given050", "given000"],
    "test":     ["p", "i", "none"]
}

def get_title(trait):
    """ Return the title of the trait """
    try:
        return title[trait]
    except KeyError:
        return trait

def get_traits(mode):
    """ Return the traits for the mode """
    try:
        return traits[mode]
    except KeyError as exc:
        raise ValueError(f"{mode} not found") from exc

def get_mechanisms(mode):
    """ Return the mechanisms for the mode """
    try:
        return mechanisms[mode]
    except KeyError:
        return mechanisms["default"]
