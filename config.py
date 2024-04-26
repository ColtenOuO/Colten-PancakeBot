from pydantic import BaseModel
from orjson import loads, dumps, OPT_INDENT_2


class MongoDBConfig(BaseModel):
    url: str = ""
    db_name: str = "colten-pancake"


class APIConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class Config(BaseModel):
    token: str = ""
    data_dir: str = "data"
    managers: list[int] = []
    main_channel: int = 0
    mongodb: MongoDBConfig = MongoDBConfig()
    api_config: APIConfig = APIConfig()
    stock_channel: int = 0


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
STCOK_CHANNEL = config.stock_channel

MONGO_DB_URL = config.mongodb.url
MONGO_DB_NAME = config.mongodb.db_name

API_HOST = config.api_config.host
API_PORT = config.api_config.port

