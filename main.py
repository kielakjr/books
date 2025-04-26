from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import models
import schemas
import crud
from database import Session, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=List[schemas.Book])
def read_books(
    skip: int = 0,
    limit: int = 100,
    author: Optional[str] = None,
    title_contains: Optional[str] = None,
    category: Optional[str] = None,
    min_rating: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Book)
    if author:
        query = query.filter(models.Book.author == author)
    if title_contains:
        query = query.filter(models.Book.title.contains(title_contains))
    if category:
        query = query.filter(models.Book.category == category)
    if min_rating:
        query = query.filter(models.Book.rating >= min_rating)
    books = query.offset(skip).limit(limit).all()
    return books


@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.delete("/books/{book_id}", response_model=schemas.Book)
def remove_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.delete_book(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.patch("/books/{book_id}", response_model=schemas.Book)
def patch_book(book_id: int, book_update: schemas.BookUpdate,
               db: Session = Depends(get_db)):
    patched_book = crud.patch_book(db, book_id, book_update)
    if patched_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return patched_book
