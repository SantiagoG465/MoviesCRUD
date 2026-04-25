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

class ReviewBase(SQLModel):
    comment: str
    score: float
    date: str
    is_active: bool = True
    movie_id: int = Field(foreign_key="movie.id")


class Review(ReviewBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ReviewUpdate(SQLModel):
    comment: Optional[str] = None
    score: Optional[float] = None
    date: Optional[str] = None
    is_active: Optional[bool] = None