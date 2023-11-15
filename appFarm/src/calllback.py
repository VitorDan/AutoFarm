from pymongo import MongoClient
import pandas as pd
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
            aux_obj = pd.DataFrame([int(float(data["k"]["t"])/1000),float(data["k"]["o"]),float(data["k"]["h"]),float(data["k"]["l"]),float(data["k"]["c"]),float(data["k"]["v"])])
            aux_obj.columns = self.columns
            print(aux_obj)