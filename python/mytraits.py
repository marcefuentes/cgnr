
def ttr(traitset):

    if traitset == "cooperation":
        traits = ["ChooseGrain",
                  "MimicGrain",
                  "ImimicGrain",
                  "w"]
        titles = ["Partner choice",
                  "Direct\nreciprocity",
                  "Indirect\nreciprocity",
                  "Fitness"]
        rows = ["pi", "p", "i", "none"]

    elif traitset == "cooperationl":
        traits = ["ChooseGrain",
                  "Choose_ltGrain",
                  "MimicGrain",
                  "ImimicGrain",
                  "Imimic_ltGrain",
                  "qBSeen"]
        titles = ["Partner choice\n(memory 1)",
                  "Partner choice\n(lifetime)",
                  "Direct\nreciprocity",
                  "Indirect\nreciprocity\n(memory 1)",
                  "Indirect\nreciprocity\n(lifetime)",
                  "qBSeen"]
        rows = ["pi", "p", "i", "none"]

    elif traitset == "correlations":
        traits = ["r_qB_Choose_lt",
                  "r_qB_Imimic_lt",
                  "r_Choose_lt_Imimic_lt"]
        titles = traits
        rows = ["pi", "p", "i", "none"]

    elif traitset == "none":
        traits = ["qBSeen",
                  "qBSeen_byproduct",
                  "w",
                  "w_deficit"]
        titles = ["Production of $\it{B}$",
                  "Byproduct help",
                  "Fitness",
                  "Fitness deficit"]
        rows = ["given100", "given095", "given050", "given000"]

    return traits, titles, rows
