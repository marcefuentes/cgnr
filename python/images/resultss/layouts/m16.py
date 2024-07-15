"""16 plots."""

from resultss.layouts.default_layout import default_layout
from resultss.layouts.ss import S1, S2, S3, S4, S5


def m16(options):
    """All figures."""

    lang = "lang" if options["lang"] else "nolang"

    variants = [
        [
            f"{lang}_noshuffle_cost15_128",
            f"{lang}_noshuffle_cost15_128",
            f"{lang}_shuffle_cost15_128",
            f"{lang}_shuffle_cost15_128",
        ],
        [
            f"{lang}_noshuffle_cost15_4",
            f"{lang}_noshuffle_cost15_4",
            f"{lang}_shuffle_cost15_4",
            f"{lang}_shuffle_cost15_4",
        ],
        [
            f"{lang}_noshuffle_cost15_128",
            f"{lang}_noshuffle_cost15_128",
            f"{lang}_shuffle_cost15_128",
            f"{lang}_shuffle_cost15_128",
        ],
        [
            f"{lang}_noshuffle_cost15_4",
            f"{lang}_noshuffle_cost15_4",
            f"{lang}_shuffle_cost15_4",
            f"{lang}_shuffle_cost15_4",
        ],
    ]

    layout = default_layout(variants, options)

    if options["trait"] == "qBSeenmean" or options["trait"] == "wmean":
        layout["givens_control"] = [
            [options["given"], options["given"], options["given"], options["given"]],
            [options["given"], options["given"], options["given"], options["given"]],
            ["0.0", "0.0", "0.0", "0.0"],
            ["0.0", "0.0", "0.0", "0.0"],
        ]
    else:
        layout["givens"] = [
            ["1.0", "1.0", "1.0", "1.0"],
            ["1.0", "1.0", "1.0", "1.0"],
            ["0.5", "0.5", "0.5", "0.5"],
            ["0.5", "0.5", "0.5", "0.5"],
        ]

        if options["given_control"] != "0.0":
            layout["given_control"] = layout["givens"]

    layout["mechanisms"] = [["pd", "pi", "pd", "pi"] for _ in range(len(variants))]

    if "Imimic" in options["trait"]:
        layout["traits"] = [
            [None, options["trait"], None, options["trait"]] for _ in range(len(variants))
        ] 

    layout["titles_columns"] = [
        f"No shuffling\n{S1}, {S4}",
        f"No shuffling\n{S1}, {S2}, {S4}",
        f"Shuffling\n{S1}, {S4}",
        f"Shuffling\n{S1}, {S2}, {S4}",
    ]

    return layout
