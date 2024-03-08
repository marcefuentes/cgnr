
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
                  "w"]
        titles = ["Partner choice",
                  "Partner choice\nlifetime",
                  "Direct\nreciprocity",
                  "Indirect\nreciprocity",
                  "Indirect\nreciprocity\nlifetime",
                  "Fitness"]
        rows = ["i", "none"]

    elif traitset == "correlations":
        traits = ["r_qB_Choose",
                  "r_qB_Mimic",
                  "r_qB_Imimic",
                  "r_Choose_Imimic"]
        titles = ["Choose\nqB",
                  "Mimic\nqB",
                  "Imimic\nqB",
                  "Choose\nImimic"]
        rows = ["pi", "p", "i", "none"]

    elif traitset == "none":
        traits = ["qBSeen",
                  "qBSeen",
                  "w",
                  "w"]
        titles = ["Production of $\it{B}$",
                  "Byproduct help",
                  "Fitness",
                  "Fitness deficit"]
        rows = ["given100", "given095", "given050", "given000"]

    return traits, titles, rows
