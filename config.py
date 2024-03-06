from pydantic import BaseModel
from orjson import loads, dumps, OPT_INDENT_2

from typing import Optional


class MongoDBConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 27017
    username: Optional[str] = None
    password: Optional[str] = None


class Config(BaseModel):
    token: str = ""
    data_dir: str = "data"
    managers: list[int] = []
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

MONGO_DB = config.mongodb
