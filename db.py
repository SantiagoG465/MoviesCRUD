from sqlmodel import SQLModel, create_engine, Session
from fastapi import Depends
from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI

DATABASE_URL = "sqlite:///movies.db"

engine = create_engine(DATABASE_URL)


def create_all_tables(app: FastAPI):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        SQLModel.metadata.create_all(engine)
        yield
    return lifespan(app)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]