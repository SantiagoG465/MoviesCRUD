import csv
import os
from typing import Optional
from models import Movie, MovieBase, MovieUpdate
from operations_genre_csv import find_one_genre_csv

MOVIES_CSV = os.path.join(os.path.dirname(__file__), "data", "movies.csv")


def _parse_bool(val: str | bool) -> bool:
    if isinstance(val, bool):
        return val
    return str(val).strip().lower() in ("true", "1", "yes")


def _read_movies() -> list[Movie]:
    if not os.path.exists(MOVIES_CSV):
        return []
    movies = []
    with open(MOVIES_CSV, mode="r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if not row or not row.get("id"):
                continue
            movies.append(
                Movie(
                    id=int(row["id"]),
                    title=row["title"],
                    director=row["director"],
                    year=int(row["year"]),
                    watched=_parse_bool(row["watched"]),
                    genre_id=int(row["genre_id"]),
                )
            )
    return movies


def _write_movies(movies: list[Movie]) -> None:
    os.makedirs(os.path.dirname(MOVIES_CSV), exist_ok=True)
    with open(MOVIES_CSV, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file, fieldnames=["title", "director", "year", "watched", "genre_id", "id"]
        )
        writer.writeheader()
        for m in movies:
            writer.writerow(
                {
                    "title": m.title,
                    "director": m.director,
                    "year": m.year,
                    "watched": m.watched,
                    "genre_id": m.genre_id,
                    "id": m.id,
                }
            )


def create_movie_csv(movie: MovieBase) -> Movie:
    if not find_one_genre_csv(movie.genre_id):
        raise ValueError(f"Genre with id {movie.genre_id} does not exist")
    movies = _read_movies()
    next_id = max((m.id for m in movies if m.id is not None), default=0) + 1
    new_movie = Movie(
        id=next_id,
        title=movie.title,
        director=movie.director,
        year=movie.year,
        watched=movie.watched,
        genre_id=movie.genre_id,
    )
    movies.append(new_movie)
    _write_movies(movies)
    return new_movie


def show_all_movies_csv() -> list[Movie]:
    return _read_movies()


def find_one_movie_csv(id: int) -> Optional[Movie]:
    movies = _read_movies()
    for m in movies:
        if m.id == id:
            return m
    return None


def update_one_movie_csv(id: int, movie_update: MovieUpdate) -> Optional[Movie]:
    movies = _read_movies()
    for idx, m in enumerate(movies):
        if m.id == id:
            update_data = movie_update.model_dump(exclude_unset=True)
            if "genre_id" in update_data and update_data["genre_id"] is not None:
                if not find_one_genre_csv(update_data["genre_id"]):
                    raise ValueError(f"Genre with id {update_data['genre_id']} does not exist")
            for key, value in update_data.items():
                if value is not None:
                    setattr(m, key, value)
            movies[idx] = m
            _write_movies(movies)
            return m
    return None


def kill_one_movie_csv(id: int) -> Optional[Movie]:
    movies = _read_movies()
    for idx, m in enumerate(movies):
        if m.id == id:
            deleted = movies.pop(idx)
            _write_movies(movies)
            return deleted
    return None


def filter_movies_by_genre_csv(genre_id: int) -> list[Movie]:
    movies = _read_movies()
    return [m for m in movies if m.genre_id == genre_id]
