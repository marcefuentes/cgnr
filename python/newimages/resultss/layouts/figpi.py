"""Plots for partner choice plus reciprocity."""

from resultsm.default_data import default_data_ipi, get_subtitles


def figpi(data):
    """Plots for partner choice plus reciprocity."""

    mechanisms = ["pd", "pi", "pd", "pi"]
    variants_common = [
        f"{data['lang']}_noshuffle_cost15",
        f"{data['lang']}_noshuffle_cost15",
        f"{data['lang']}_shuffle_cost15",
        f"{data['lang']}_shuffle_cost15",
    ]
    trait = data["traits"]
    default_data_ipi(data, mechanisms, variants_common)
    data["titles_columns"] = get_subtitles(
        data["titles_columns"], variants_common, mechanisms
    )

    if trait == "ImimicGrainmean":
        data["traits"] = [
            ["nothing", "ImimicGrainmean", "nothing", "ImimicGrainmean"]
            for _ in data["variants"]
        ]
    elif trait == "Imimic_ltGrainmean":
        data["traits"] = [
            ["nothing", "Imimic_ltGrainmean", "nothing", "Imimic_ltGrainmean"]
            for _ in data["variants"]
        ]
