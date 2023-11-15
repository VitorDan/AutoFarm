from binance import ThreadedWebsocketManager
from binance.enums import *
from callbacks import MongoSave
class Binance_Data_Reciver():
    def __init__(self,api_key, api_secret):
       self.socket = ThreadedWebsocketManager(api_key, api_secret)
       self.socket.start()
    def worker_recive(self):
        msg_hadler = MongoSave()
        self.socket.start_kline_socket(callback=msg_hadler.save,symbol='BTCUSDT',interval=KLINE_INTERVAL_1MINUTE)
        self.socket.join()
    def run(self):  
        self.worker_recive()