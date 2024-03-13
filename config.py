from pydantic import BaseModel
from orjson import loads, dumps, OPT_INDENT_2

from typing import Optional


class MongoDBConfig(BaseModel):
    url: str = ""
    db_name: str = "colten-pancake"


class Config(BaseModel):
    token: str = ""
    data_dir: str = "data"
    managers: list[int] = []
    main_channel: int = 0
    mongodb: MongoDBConfig = MongoDBConfig()


try:
    with open("config.json", "rb") as file:
        config = Config(**loads(file.read()))
except:
    config = Config()
    with open("config.json", "wb") as file:
        file.write(dumps(config.model_dump(), option=OPT_INDENT_2))
    input("Please go to edit your config.json")
    exit(0)

TOKEN = config.token
DATA_DIR = config.data_dir
MANAGERS = config.managers
MAIN_CHANNEL = config.main_channel

MONGO_DB_URL = config.mongodb.url
MONGO_DB_NAME = config.mongodb.db_name
