from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException
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
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db_review = models.Review(comment=review.comment, rating=review.rating, book_id=book_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    reviews = db.query(models.Review).filter(models.Review.book_id == book_id).all()
    if reviews:
        average_rating = sum(r.rating for r in reviews) / len(reviews)
        book.rating = round(average_rating, 2)
    else:
        book.rating = None

    db.commit()
    db.refresh(book)

    return db_review


def get_reviews_for_book(db: Session, book_id: int):
    return db.query(models.Review).filter(models.Review.book_id == book_id).all()


def patch_review(db: Session, review_id: int, review_patch: schemas.ReviewUpdate):
    db_review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    book = db.query(models.Book).filter(models.Book.id == db_review.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    for key, value in review_patch.model_dump(exclude_unset=True).items():
        setattr(db_review, key, value)

    db.commit()
    db.refresh(db_review)

    reviews = db.query(models.Review).filter(models.Review.book_id == book.id).all()
    if reviews:
        average_rating = sum(r.rating for r in reviews) / len(reviews)
        book.rating = round(average_rating, 2)
    else:
        book.rating = None

    db.commit()
    db.refresh(book)

    return db_review


def delete_review(db: Session, review_id: int):
    db_review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    book = db.query(models.Book).filter(models.Book.id == db_review.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(db_review)
    db.commit()

    reviews = db.query(models.Review).filter(models.Review.book_id == book.id).all()
    if reviews:
        average_rating = sum(r.rating for r in reviews) / len(reviews)
        book.rating = round(average_rating, 2)
    else:
        book.rating = None

    db.commit()
    db.refresh(book)

    return db_review
