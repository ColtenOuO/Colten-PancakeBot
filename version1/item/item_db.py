from pymongo import MongoClient
import json


class item_system:
    class user_information:
        def __init__(self) -> None:
            self.id = ""
            self.exp = 0
            self.bonus = 0
            self.skill = 0
            self.item = []
    def __init__(self) -> None:
        with open('token.json') as f:
            tokens = json.load(f)
        self.client = MongoClient(tokens['db_client'])
    def user_query(self,discord_id: str) -> None:
        for USER in self.client.pythondb["item_data"].find():
            if( USER["discord_id"] == discord_id ): return USER
        return None
    def user_adding(self,discord_id) -> None:
        new_user = {
            "discord_id": discord_id,
            "exp": 10,
            "skill": 0,
            "item": []
        }
        self.client.pythondb["item_data"].insert_one(new_user)
    def exp_update(self,db,discord_id,exp_get):
        target_user = db.user_query(discord_id)
        target_data = { 'discord_id': discord_id }
        new_data = { '$set': { 'exp': target_user["exp"] + exp_get } }
        db.client.pythondb["item_data"].update_one(target_data,new_data)

