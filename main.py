from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
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
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
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


@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book_endpoint(book_id: int, book_update: schemas.BookUpdate,
                         db: Session = Depends(get_db)):
    updated_book = crud.update_book(db, book_id, book_update)
    if updated_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book
