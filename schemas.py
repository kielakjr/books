from pydantic import BaseModel, Field, field_validator
from typing import Optional, List


class BookBase(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    rating: Optional[float] = None
    description: Optional[str] = None

    @field_validator('rating')
    def round_rating(cls, v):
        if v is not None:
            return round(v, 2)
        return v


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    title: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[float] = None
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
