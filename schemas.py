from pydantic import BaseModel
from typing import Optional


class BookBase(BaseModel):
    title: str
    author: str
    category: str
    rating: int
    description: str


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    title: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[int] = None
    description: Optional[str] = None


class Book(BookBase):
    id: int

    class Config:
        orm_mode = True
