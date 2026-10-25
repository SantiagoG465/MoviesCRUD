from typing import Optional
from pydantic import BaseModel, Field


class GenreBase(BaseModel):
    name: str = Field(min_length=3, max_length=50)


class Genre(GenreBase):
    id: Optional[int] = None


class GenreUpdate(BaseModel):
    name: Optional[str] = None


class DirectorBase(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    nationality: str = Field(min_length=2, max_length=60)
    is_active: bool = True


class Director(DirectorBase):
    id: Optional[int] = None


class DirectorUpdate(BaseModel):
    name: Optional[str] = None
    nationality: Optional[str] = None
    is_active: Optional[bool] = None


class MovieBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    director_id: int
    year: int = Field(gt=1888, le=2026)
    watched: bool = False
    genre_id: int


class Movie(MovieBase):
    id: Optional[int] = None


class MovieUpdate(BaseModel):
    title: Optional[str] = None
    director_id: Optional[int] = None
    year: Optional[int] = None
    watched: Optional[bool] = None
    genre_id: Optional[int] = None
