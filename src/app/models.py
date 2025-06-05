from pydantic import BaseModel


class StringItem(BaseModel):
    value: str
    id: str


class PostValue(BaseModel):
    value: str
