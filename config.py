from pydantic import BaseModel
from orjson import loads, dumps, OPT_INDENT_2


class Config(BaseModel):
    token: str = ""
    data_dir: str = "data"
    managers: list[int] = []


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
