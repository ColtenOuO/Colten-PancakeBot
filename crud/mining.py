from pymongo import MongoClient
import json

with open('token.json') as f:
    tokens = json.load(f)
client = MongoClient(tokens['db_client'])

class MiningData:
    def insert_new_one(self,discord_id: int,user_time):
        new_data = {
            "discord_id": discord_id,
            "last_time": user_time
        }
        client.pythondb['mining_data'].insert_one(new_data)
    def query_user_time(self,discord_id: int):
        for USER in client.pythondb['mining_data'].find():
            if( USER['discord_id'] == discord_id ): return USER['time']
        return None
    def update_one(self,discord_id: int,user_time):
        target_data = { "discord_id": discord_id }
        new_data = { '$set': { 'time': user_time } }
        client.pythondb['mining_data'].update_one(target_data,new_data)
    
