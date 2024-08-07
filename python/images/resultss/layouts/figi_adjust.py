"""Plots for reciprocity."""

from resultsm.add_default_data import add_default_data_ipi, get_subtitles


def figi_adjust(data):
    """Plots for reciprocity."""

    mechanisms = ["d", "i", "d", "i", "i"]
    variants_common = [
        "nolang_noshuffle_cost15",
        "lang_noshuffle_cost15",
        "nolang_shuffle_cost15",
        "nolang_shuffle_cost15",
        "lang_shuffle_cost15",
    ]
    trait = data["traits"]
    add_default_data_ipi(data, mechanisms, variants_common)
    data["titles_columns"] = get_subtitles(
        data["titles_columns"], variants_common, mechanisms
    )

    if trait == "ImimicGrainmean":
        data["traits"] = [
            ["nothing", "nothing", "nothing", "ImimicGrainmean", "ImimicGrainmean"]
            for _ in data["variants"]
        ]
    elif trait == "Imimic_ltGrainmean":
        data["traits"] = [
            [
                "nothing",
                "Imimic_ltGrainmean",
                "nothing",
                "nothing",
                "Imimic_ltGrainmean",
            ]
            for _ in data["variants"]
        ]
