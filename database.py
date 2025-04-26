from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///./devbook.db")

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
