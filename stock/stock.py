from pymongo import MongoClient
import json
with open('token.json') as f:
    tokens = json.load(f)
    client = MongoClient(tokens['db_client'])

class StockSystem:
    def insert_new(self,id: str,price: int):
        new_stock = {
            id: price,
            "buy": 0,
            "sell": 0
        }
        client.pythondb["stock"].insert_one(new_stock)
    def update_one(self,id: str,price: int):
        target_data = { id: self.get_price(id) }
        new_data = { '$set': { id: self.get_price(id) + price } }
        client.pythondb['stock'].update_one(target_data,new_data)
        return

    def __init__(self) -> None:
        self.stock_list = ["高睿屬實有料股份有限公司", "YEE問題不大股份有限公司", "美麗橋建設股份有限公司"]
        cnt = 0
        for DATA in client.pythondb['stock'].find(): cnt += 1
        if( cnt == 0 ):
            self.insert_new('1',23)
            self.insert_new('2',23)
            self.insert_new('3',23) 
    def get_price(self,stock_id: str) -> int:
        if( client.pythondb['stock'][stock_id] == None ): return -1 # Not Found
        for DATA in client.pythondb['stock'].find():
            if( DATA[stock_id] != None ): return DATA[stock_id]
        