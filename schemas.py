from pydantic import BaseModel, Field
from typing import Optional


class BookBase(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    rating: int = Field(..., ge=0, le=10)
    description: str = Field(..., min_length=1)


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
