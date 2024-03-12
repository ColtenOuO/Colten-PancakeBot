from pydantic import BaseModel

class EmbedField(BaseModel):
    name: str = ""
    value: str = ""
    inline: bool = False
