from app.src.database import db_client as db
import pandas as pd
def get_samples(col_name,size=None):
    client = db['AutoFarm'][col_name]
    if size is None:
        df = pd.DataFrame(client.find({},{"_id": 0}))
    else:
        df = pd.DataFrame(client.find({},{"_id": 0}).limit(size))
    return df 
def insert_samples(df,col_name):
    client = db['AutoFarm']
    collection = client.create_collection(col_name, timeseries={ 'timeField': 'OpenTime' })
    collection.insert_many(df.to_dict('records'))
    