from typing import Generator
from sqlmodel import SQLModel, create_engine, Session
from fastapi import FastAPI

DATABASE_URL = "sqlite:///./universidad.db"
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

def create_db_and_tables(app: FastAPI | None = None):
    """
    Crea la base de datos (universidad.db) y todas las tablas definidas en models.py.
    Esta función se ejecuta al inicio de la aplicación (@app.on_event("startup")).
    """

    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """
    Dependencia de FastAPI que proporciona una nueva sesión de base de datos
    para cada solicitud (endpoint). Asegura que la sesión se cierre correctamente.
    """
    with Session(engine) as session:
        yield session