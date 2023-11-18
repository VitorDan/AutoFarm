from binance import ThreadedWebsocketManager
from binance.enums import *
import pandas as pd
import numpy as np
from datetime import datetime
from pymongo import MongoClient
class MongoSave():
    def __init__(self,database = 'AutoFarmBase',pair="ADAUSDT"):
        self.mongo_url = "mongodb://root:example@localhost:27017/"
        self.mongo_db = database
        self.mongo_coll = pair
        self.columns = columns = ["OpenTime","Open","High","Low","Close","Volume"]
    def print_handler(self,msg):
        print(msg)
    def save(self,data):
        if data["k"]["x"]:
            arr = np.array([
                    [int(float(data["k"]["t"])/1000)],
                    [float(data["k"]["o"])],
                    [float(data["k"]["h"])],
                    [float(data["k"]["l"])],
                    [float(data["k"]["c"])],
                    [float(data["k"]["v"])]
                ]).T
            print(arr.shape)
            aux_obj = pd.DataFrame(arr)
            aux_obj.columns = self.columns 
            aux_obj['OpenTime'] = pd.to_datetime(aux_obj['OpenTime'].apply(lambda timestamp: datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')),format='%Y-%m-%d %H:%M')
            print(aux_obj.dtypes)
            with MongoClient(self.mongo_url) as db_client:
                db = db_client[self.mongo_db]
                client = db[self.mongo_coll]
                client.insert_many(aux_obj.to_dict('records'))
def msg(e):
    print(e)
mongo = MongoSave()



socket = ThreadedWebsocketManager(api_key, secret_key)
socket.start()
socket.start_kline_socket(callback=mongo.save,symbol='ADAUSDT',interval=KLINE_INTERVAL_1MINUTE)
# streams = ['btcusdt@depth20@100ms']
# socket.start_multiplex_socket(callback=msg, streams=streams)


socket.join()
