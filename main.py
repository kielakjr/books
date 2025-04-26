from fastapi import FastAPI
from database import engine
import models

models.Base.metadata.create_all(engine)

app = FastAPI()


@app.get("/")
def index():
    return {"message": "Hello, DevBook!"}
