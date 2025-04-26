from pydantic import BaseModel, Field, field_validator
from typing import Optional, List


class BookBase(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    rating: Optional[float] = None
    description: Optional[str] = None


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    description: Optional[str] = None


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None


class ReviewBase(BaseModel):
    rating: float = Field(..., ge=0, le=10)
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class Review(ReviewBase):
    id: int
    book_id: int

    class Config:
        from_attribtues = True


class Book(BookBase):
    id: int
    reviews: List[Review] = []

    class Config:
        from_attribtues = True
