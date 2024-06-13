"""Creates a zmatrix for the given time, dataframe, and trait."""

import pandas as pd


def get_zmatrix(t, df, trait):
    """Returns the zmatrix for a given time, dataframe, and trait."""

    if trait not in df.columns:
        print(f"Trait {trait} not in the dataframe.")
        return None
    m = df.Time == t
    params = {
        "values": trait,
        "index": "alpha",
        "columns": "logES",
    }
    zmatrix = pd.pivot(df.loc[m], **params)
    zmatrix = zmatrix.sort_index(axis=0, ascending=False)
    zmatrix = zmatrix.to_numpy()
    return zmatrix
