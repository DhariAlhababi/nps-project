import os
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=False)

def create_db_and_tables():
    from .models import Park, Campground, Alert
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)
