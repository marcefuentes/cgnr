
import pandas as pd

def get_Z(t, df, trait):
    m = df.Time == t
    Z = pd.pivot(df.loc[m],
                 values=trait,
                 index="alpha",
                 columns="logES")
    Z = Z.sort_index(axis=0, ascending=False)
    Z = Z.to_numpy()
    return Z

