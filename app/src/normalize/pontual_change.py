def change_volume(df):
    df.loc[df['Volume'] < 1, 'Volume'] = df['Volume'].median()
    return df
def time_set_unit(df):
    df['OpenTime'] = pd.to_datetime(df['OpenTime'],format='%Y-%m-%d %H:%M')
    return df