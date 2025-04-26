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


def update_book(db: Session, book_id: int, book_update: schemas.BookUpdate):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        return None

    if book_update.title:
        book.title = book_update.title
    if book_update.author:
        book.author = book_update.author
    if book_update.category:
        book.category = book_update.category
    if book_update.rating or book_update.rating == 0:
        book.rating = book_update.rating
    if book_update.description:
        book.description = book_update.description

    db.commit()
    db.refresh(book)
    return book
