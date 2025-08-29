from sqlmodel import Session, create_engine, SQLModel

from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.getenv("DB_URL")

engine = create_engine(DB_URL, echo=True)


def get_session():
    """Creates a session to the database"""
    with Session(engine) as session:
        yield session


def init_db():
    """Creates the database tables"""
    SQLModel.metadata.create_all(engine)
