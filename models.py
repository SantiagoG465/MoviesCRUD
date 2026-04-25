from typing import Optional
from sqlmodel import SQLModel, Field


class MovieBase(SQLModel):
    title: str
    director: str
    year: int
    genre: str
    rating: float
    watched: bool = False


class Movie(MovieBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class MovieUpdate(SQLModel):
    title: Optional[str] = None
    director: Optional[str] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    rating: Optional[float] = None
    watched: Optional[bool] = None