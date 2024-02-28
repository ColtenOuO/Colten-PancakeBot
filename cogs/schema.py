from pydantic import BaseModel

class CogConfig(BaseModel):
    path: str
    description: str = ""
    load_on_start: bool = False
