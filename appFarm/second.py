from binance import AsyncClient
from binance.enums import *
import pandas as pd
import asyncio
from datetime import datetime
from pymongo import MongoClient
api_key = "Fj6SxfmYteRU61SYP9G2T8msbezPDCQFY9iE54guuOtc8eWKF6HdhzX4eIYaK2CR"
secret_key= "DUYD9o42PuYg5v81kaxMJKFW19USR6IS52ZyvHLML5DpC5XkUcuDNEyaUE1EaK8v"
async def get_coin_historical(pair = "ADAUSDT"):
    client = await AsyncClient.create(api_key, secret_key, testnet=False)
    klines = await client.get_historical_klines(pair, KLINE_INTERVAL_1MINUTE, '2023-01-01T00:00:00Z')
    klines = pd.DataFrame(klines)
    await client.close_connection()
    klines.columns = ["OpenTime","Open","High","Low","Close","Volume","CloseTime","QAV","NumTrades","TBBAV","TBQAV","Ignore"]
    klines = klines[["OpenTime","Open","High","Low","Close","Volume"]]
    klines['OpenTime'] = klines['OpenTime'] / 1000 
    klines['OpenTime'] = pd.to_datetime(klines['OpenTime'].apply(lambda timestamp: datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')),format='%Y-%m-%d %H:%M')
    print(klines)    
    with MongoClient("mongodb://root:example@localhost:27017/") as db_client:
        db = db_client['AutoFarmBase']
        client = db[pair]
        client.insert_many(klines.to_dict('records'))

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_coin_historical('BTCUSDT'))