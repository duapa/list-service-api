from pydantic import BaseModel


class PostValue(BaseModel):
    value: str
