"""Creates a zmatrix for the given time, dataframe, and trait."""

import pandas as pd


def get_zmatrix(t, df, trait, rows, cols):
    """Returns the zmatrix for a given time, dataframe, and trait."""

    df = df.loc[df.Time == t]
    zmatrix = pd.pivot_table(
        df,
        values=trait,
        index=rows,
        columns=cols,
        fill_value=0,
    )
    zmatrix = zmatrix.sort_index(axis=0, ascending=False)
    zmatrix = zmatrix.to_numpy()
    return zmatrix
