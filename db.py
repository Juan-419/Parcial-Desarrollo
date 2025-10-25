from typing import Generator
from sqlmodel import SQLModel, create_engine, Session
from fastapi import FastAPI

DATABASE_URL = "sqlite:///./universidad.db"
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

def create_db_and_tables(app: FastAPI | None = None):

    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session