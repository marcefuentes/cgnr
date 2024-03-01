
def ttr(traitset):

    if traitset == "cooperation":
        traits = ["ChooseGrainmean",
                  "MimicGrainmean",
                  "ImimicGrainmean",
                  "wmean"]
        titles = ["Partner choice",
                  "Direct\nreciprocity",
                  "Indirect\nreciprocity",
                  "Fitness"]
        rows = ["pil", "pl", "il", "none"]

    elif traitset == "correlations":
        traits = ["r_qB_Choose",
                  "r_qB_Mimic",
                  "r_qB_Imimic",
                  "r_Choose_Imimic"]
        titles = ["Choose\nqB",
                  "Mimic\nqB",
                  "Imimic\nqB",
                  "Choose\nImimic"]
        rows = ["pil", "pl", "il", "none"]

    elif traitset == "none":
        traits = ["qBSeenmean",
                  "qBSeenmean",
                  "wmean",
                  "wmean"]
        titles = ["Production of $\it{B}$",
                  "Byproduct help",
                  "Fitness",
                  "Fitness deficit"]
        rows = ["given100", "given095", "given050", "given000"]

    return traits, titles, rows
