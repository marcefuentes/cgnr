""" Data layout. """


folder_variant_list = [
        ["nolang_noshuffle_cost15_128", "nolang_shuffle_cost15_128"],
        ["nolang_noshuffle_cost15_4", "nolang_shuffle_cost15_4"],
    ]
folder_variant_control_list = folder_variant_list

mechanism = "p"
given = "1.0"
mechanism_control = "none"
given_control = given

nrows = len(folder_variant_list)
ncols = len(folder_variant_list[0]) if nrows > 0 else 0

mechanism_list = [[mechanism for _ in range(ncols)] for _ in range(nrows)]
mechanism_control_list = [[mechanism_control for _ in range(ncols)] for _ in range(nrows)]
given_list = [[given for _ in range(ncols)] for _ in range(nrows)]
given_control_list = [[given_control for _ in range(ncols)] for _ in range(nrows)]

data_layout = {
    "column_titles": ["No shuffling", "Shuffling"],
    "folder_given": given_list,
    "folder_given_control": given_control_list,
    "folder_mechanism": mechanism_list,
    "folder_mechanism_control": mechanism_control_list,
    "folder_variant": folder_variant_list,
    "folder_variant_control": folder_variant_control_list,
    "given": given,
    "row_titles": ["", ""],
}
