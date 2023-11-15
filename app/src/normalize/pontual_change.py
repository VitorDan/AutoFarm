import pandas as pd
def change_volume(df):
    df["Volume"] = df["Volume"].rolling(210).mean()
    return df
def time_set_unit(df):
    df['OpenTime'] = pd.to_datetime(df['OpenTime'],format='%Y-%m-%d %H:%M')
    return df