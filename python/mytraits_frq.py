
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
        rows = ["pil", "pl", "il", "none"]

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
