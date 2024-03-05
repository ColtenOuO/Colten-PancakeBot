from pymongo import MongoClient
import json

class User:
    def __init__(self, discord_id: str, money: int = 0, pancake: int = 0) -> None:
        self.discord_id = discord_id
class database:
    class update_user:
        def __init__(self, add_money_val: int, pancake: int) -> None:
            self.add_money_val = add_money_val
            self.pancake = pancake
        def update_money(self, db: 'database', discord_id: str, money: int, ) -> None:
            USER_DATA = db.User_Query(discord_id)
            target_data = { 'discord_id': discord_id }
            new_data = { '$set': { 'money': USER_DATA["money"] + self.add_money_val } }
            db.client.pythondb["discord_user_data"].update_one(target_data,new_data)

    def __init__(self) -> None:
        with open('token.json') as f:
            tokens = json.load(f)
        self.client = MongoClient(tokens['db_client'])
    
    def Register_Query(self, user_id: str) -> bool:
        all_user_data = self.client.pythondb["discord_user_data"].find()
        for USER in all_user_data:
            if( USER["discord_id"] == user_id ): return True
        return False
    
    def Registered(self, user_id: str) -> None:
        new_user = User(user_id)
        Insert_objecgt = {
            "discord_id": new_user.discord_id,
            "money": 0,
            "pancake": 0
        }
        self.client.pythondb["discord_user_data"].insert_one(Insert_objecgt)
    
    def User_Query(self, user_id: str) -> User:
        all_user_data = self.client.pythondb["discord_user_data"].find()
        for USER in all_user_data:
            if( USER["discord_id"] == user_id ): return USER
        return None

