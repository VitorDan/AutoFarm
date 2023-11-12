from app.src.models import autofarmbase as atdb
import pandas as pd 

df = pd.read_csv('./data/ada_process.csv')

df['OpenTime'] = pd.to_datetime(df['OpenTime'],format='%Y-%m-%d %H:%M')



df.loc[df['Volume'] < 1, 'Volume'] = df['Volume'].median()
atdb.insert_samples(df,'ADAUSDT')


# df = atdb.get_samples('ADAUSDT')
print(df.describe())
print(df.dtypes)
# from pymongo import MongoClient




# mongo_url = "mongodb://root:example@localhost:27017/"
# db_client = MongoClient(mongo_url)

# auto_farm_base_client =  db_client['AutoFarmBase']
# auto_farm_client = db_client['AutoFarm']



# collection = auto_farm_base_client.create_collection('ADAUSDT', timeseries={ 'timeField': 'OpenTime' })
# collection.insert_many(df.to_dict('records'))

# df.to_csv('ameba.csv')
# df = pd.DataFrame(auto_farm_base_client['ADAUSDT'].find({},{"_id": 0}))