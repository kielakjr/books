from sqlalchemy.orm import Session
from typing import List, Optional
import models
import schemas


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(db: Session,
              skip: int = 0, limit: int = 100) -> List[models.Book]:
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int) -> Optional[models.Book]:
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def delete_book(db: Session, book_id: int):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book:
        db.delete(book)
        db.commit()
        return book
    return None


def patch_book(db: Session, book_id: int, book_update: schemas.BookUpdate):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        return None

    patched_data = book_update.model_dump(exclude_unset=True)
    for key, value in patched_data.items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return book


def create_review(db: Session, book_id: int, review: schemas.ReviewCreate):
    review = models.Review(book_id=book_id, rating=review.rating, comment=review.comment)
    db.add(review)
    db.commit()
    db.refresh(review)

    return review


def get_reviews_for_book(db: Session, book_id: int):
    return db.query(models.Review).filter(models.Review.book_id == book_id).all()
