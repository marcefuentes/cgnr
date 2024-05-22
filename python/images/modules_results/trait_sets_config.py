""" Store the columns and rows for the different trait_sets of the figure """

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

trait_map = {
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
