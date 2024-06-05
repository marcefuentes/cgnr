""" Data layout. """

variant_list = [
    ["nolang_noshuffle_cost15_128", "nolang_shuffle_cost15_128"],
    ["nolang_noshuffle_cost15_4", "nolang_shuffle_cost15_4"],
]
variant_control_list = variant_list

mechanism = "p"
given = "1.0"
mechanism_control = "none"
given_control = given

nrows = len(variant_list)
ncols = len(variant_list[0]) if nrows > 0 else 0

mechanism_list = [[mechanism for _ in range(ncols)] for _ in range(nrows)]
mechanism_control_list = [
    [mechanism_control for _ in range(ncols)] for _ in range(nrows)
]
given_list = [[given for _ in range(ncols)] for _ in range(nrows)]
given_control_list = [[given_control for _ in range(ncols)] for _ in range(nrows)]

default = {
    "column_titles": ["No shuffling", "Shuffling"],
    "folder_given": given_list,
    "folder_given_control": given_control_list,
    "folder_mechanism": mechanism_list,
    "folder_mechanism_control": mechanism_control_list,
    "folder_variant": variant_list,
    "folder_variant_control": variant_control_list,
    "given": given,
    "row_titles": ["", ""],
}

given_list = [["1.0", "1.0"], ["0.5", "0.5"], ["0.0", "0.0"]]
given_control_list = [[None, 0.0], [None, "0.0"], [None, "0.0"]]
mechanism = "none"
mechanism_list = [[mechanism, mechanism], [mechanism, mechanism], [mechanism, mechanism]]
mechanism_control_list = [[None, mechanism], [None, mechanism], [None, mechanism]]
variant = "nolang_noshuffle_cost15_4"
variant_list = [[variant, variant], [variant, variant], [variant, variant]]
variant_control_list = [[None, variant], [None, variant], [None, variant]]

figure_2 = {
    "column_titles": ["Fitness", "Fitness\nrelative to optimum"],
    "folder_given": given_list,
    "folder_given_control": given_control_list,
    "folder_mechanism": mechanism_list,
    "folder_mechanism_control": mechanism_control_list,
    "folder_variant": variant_list,
    "folder_variant_control": variant_control_list,
    "given": given,
    "row_titles": ["", ""],
}

data_layout = figure_2
