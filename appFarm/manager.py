import pandas as pd 
import numpy as np
import pandas_ta as ta

from pymongo import MongoClient


candle_patherns = [
    "2crows",
    "3blackcrows",
    "3inside",
    "3linestrike",
    "3outside",
    "3starsinsouth",
    "3whitesoldiers",
    "abandonedbaby",
    "advanceblock",
    "belthold",
    "breakaway",
    "closingmarubozu",
    "concealbabyswall",
    "counterattack",
    "darkcloudcover",
    "doji",
    "dojistar",
    "dragonflydoji",
    "engulfing",
    "eveningdojistar",
    "eveningstar",
    "gapsidesidewhite",
    "gravestonedoji",
    "hammer",
    "hangingman",
    "harami",
    "haramicross",
    "highwave",
    "hikkake",
    "hikkakemod",
    "homingpigeon",
    "identical3crows",
    "inneck",
    "inside",
    "invertedhammer",
    "kicking",
    "kickingbylength",
    "ladderbottom",
    "longleggeddoji",
    "longline",
    "marubozu",
    "matchinglow",
    "mathold",
    "morningdojistar",
    "morningstar",
    "onneck",
    "piercing",
    "rickshawman",
    "risefall3methods",
    "separatinglines",
    "shootingstar",
    "shortline",
    "spinningtop",
    "stalledpattern",
    "sticksandwich",
    "takuri",
    "tasukigap",
    "thrusting",
    "tristar",
    "unique3river",
    "upsidegap2crows",
    "xsidegap3methods"
]


mongo_url = "mongodb://root:example@localhost:27017/"
db = MongoClient(mongo_url)

def get_samples(col_name,size=None):
    client = db['AutoFarmBase'][col_name]
    if size is None:
        df = pd.DataFrame(client.find({},{"_id": 0}))
    else:
        df = pd.DataFrame(client.find({},{"_id": 0, "Volume":0}).limit(size))
    return df 
def change_volume(df):
    df["Volume"] = df["Volume"].rolling(210).mean()
    return df
def time_set_unit(df):
    df['OpenTime'] = pd.to_datetime(df['OpenTime'],format='%Y-%m-%d %H:%M')
    return df

def insert_samples(df,col_name):
    client = db['AFarmCandlePathern']
    collection = client.create_collection(col_name)
    collection.insert_many(df.to_dict('records'))



df = get_samples('ADAUSDT',800000)
df = time_set_unit(df)
df = change_volume(df)
df = df.set_index('OpenTime')
df = df.sort_index()
df = df.dropna()

n_data = df.ta.cdl_pattern(name=candle_patherns)
n_data.columns = candle_patherns
n_data /= 100
df = pd.concat([df,n_data],axis=1)
print(df.sample(1000))

insert_samples(df,'ADAUSDT')

