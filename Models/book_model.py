from pydantic import BaseModel


class BookModel(BaseModel):
    name: str
    author: str
    pages: int