from fastapi import FastAPI
from database import Book, session

app = FastAPI()


@app.get("/")
def index():
    return {"message": "Hello, DevBook!"}
