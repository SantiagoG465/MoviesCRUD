from typing import Optional
from sqlmodel import SQLModel, Field

class GenreBase(SQLModel):
    name: str = Field(min_length=3, max_length=50)


class Genre(GenreBase):
    id: Optional[int] = None


class GenreUpdate(SQLModel):
    name: Optional[str] = None

class MovieBase(SQLModel):
    title: str = Field(min_length=1, max_length=100)
    director: str = Field(min_length=3, max_length=100)
    year: int = Field(gt=1888, le=2026)
    watched: bool = False
    genre_id: int  #


class Movie(MovieBase):
    id: Optional[int] = None


class MovieUpdate(SQLModel):
    title: Optional[str] = None
    director: Optional[str] = None
    year: Optional[int] = None
    watched: Optional[bool] = None
    genre_id: Optional[int] = None


class UserBase(SQLModel):
    name: str = Field(min_length=3, max_length=100)
    email: str = Field(min_length=5, max_length=100)
    is_active: bool = True


class User(UserBase):
    id: Optional[int] = None


class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None