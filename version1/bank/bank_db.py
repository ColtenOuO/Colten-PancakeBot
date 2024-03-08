from pymongo import MongoClient
import json

class bank_system:
    def __init__(self) -> None:
        with open('token.json') as f:
            tokens = json.load(f)
        self.client = MongoClient(tokens['db_client'])
    def user_query(self,discord_id: str) -> None:
        for USER in self.client.pythondb["bank_data"].find():
            if( USER["discord_id"] == discord_id ): return USER
        return None
    def user_adding(self,discord_id):
        new_user = {
            "discord_id": discord_id,
            "safe_box": 0,
            "item": []
        }
        self.client.pythondb["item_data"].insert_one(new_user)
    def update_safe_box(slef,discord_id: str) -> None:
        for in

