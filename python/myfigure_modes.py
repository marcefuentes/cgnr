
# Purpose: Store the traits and rows for the different modes of the figure

title = {
    "ChooseGrain":          "Partner choice",
    "Choose_ltGrain":       "Partner choice\n(lifetime)",
    "MimicGrain":           "Direct\nreciprocity",
    "ImimicGrain":          "Indirect\nreciprocity",
    "Imimic_ltGrain":       "Indirect\nreciprocity\n(lifetime)",
    "qBSeen":               "Production of $\it{B}$",
    "qBSeen_byproduct":     "Byproduct help",
    "w":                    "Fitness",
    "w_deficit":            "Fitness deficit",
    "r_qB_Choose_lt":       "$\it{B}$ - partner choice\n(lifetime)",
    "r_qB_Imimic_lt":       "$\it{B}$ - indirect\nreciprocity (lifetime)",
    "r_Choose_lt_Imimic_lt": "Correlation: partner choice (lifetime) and indirect reciprocity (lifetime)"
}

traits = {
    "cooperation":  ["ChooseGrain", "MimicGrain", "ImimicGrain", "w"],
    "cooperationl": ["ChooseGrain", "Choose_ltGrain", "MimicGrain", "ImimicGrain", "Imimic_ltGrain", "qBSeen"],
    "correlations": ["r_qB_Choose_lt", "r_qB_Imimic_lt", "r_Choose_lt_Imimic_lt"],
    "none":         ["qBSeen", "qBSeen_byproduct", "w", "w_deficit"],
    "test":         ["qBSeen", "w"]
}

mechanisms = {
    "cooperation":  ["pi", "p", "i", "none"],
    "cooperationl": ["pi", "p", "i", "none"],
    "correlations": ["pi", "p", "i", "none"],
    "none":         ["given100", "given095", "given050", "given000"],
    "test":         ["p", "i", "none"]
}

def get_title(trait):
    try:
        return title[trait]
    except KeyError:
        raise ValueError(f"{trait} not found")

def get_traits(mode):
    try:
        return traits[mode]
    except KeyError:
        raise ValueError(f"{mode} not found")

def get_mechanisms(mode):
    try:
        return mechanisms[mode]
    except KeyError:
        raise ValueError(f"{mode} not found")

