import csv
import os
from typing import Optional
from models import Genre, GenreBase, GenreUpdate

GENRES_CSV = os.path.join(os.path.dirname(__file__), "data", "genres.csv")
MOVIES_CSV = os.path.join(os.path.dirname(__file__), "data", "movies.csv")


def _read_genres() -> list[Genre]:
    if not os.path.exists(GENRES_CSV):
        return []
    genres = []
    with open(GENRES_CSV, mode="r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if not row or not row.get("id"):
                continue
            genres.append(Genre(id=int(row["id"]), name=row["name"]))
    return genres


def _write_genres(genres: list[Genre]) -> None:
    os.makedirs(os.path.dirname(GENRES_CSV), exist_ok=True)
    with open(GENRES_CSV, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "id"])
        writer.writeheader()
        for g in genres:
            writer.writerow({"name": g.name, "id": g.id})


def _genre_has_movies(genre_id: int) -> bool:
    if not os.path.exists(MOVIES_CSV):
        return False
    with open(MOVIES_CSV, mode="r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row and row.get("genre_id") and int(row["genre_id"]) == genre_id:
                return True
    return False


def create_genre_csv(genre: GenreBase) -> Genre:
    genres = _read_genres()
    for g in genres:
        if g.name.strip().lower() == genre.name.strip().lower():
            raise ValueError(f"Genre '{genre.name}' already exists")
    next_id = max((g.id for g in genres if g.id is not None), default=0) + 1
    new_genre = Genre(id=next_id, name=genre.name)
    genres.append(new_genre)
    _write_genres(genres)
    return new_genre


def show_all_genres_csv() -> list[Genre]:
    return _read_genres()


def find_one_genre_csv(id: int) -> Optional[Genre]:
    genres = _read_genres()
    for g in genres:
        if g.id == id:
            return g
    return None


def update_one_genre_csv(id: int, genre_update: GenreUpdate) -> Optional[Genre]:
    genres = _read_genres()
    for idx, g in enumerate(genres):
        if g.id == id:
            update_data = genre_update.model_dump(exclude_unset=True)
            if "name" in update_data and update_data["name"] is not None:
                for other in genres:
                    if other.id != id and other.name.strip().lower() == update_data["name"].strip().lower():
                        raise ValueError(f"Genre '{update_data['name']}' already exists")
                g.name = update_data["name"]
            genres[idx] = g
            _write_genres(genres)
            return g
    return None


def delete_one_genre_csv(id: int) -> Optional[Genre]:
    genres = _read_genres()
    for idx, g in enumerate(genres):
        if g.id == id:
            if _genre_has_movies(id):
                raise ValueError(f"Cannot delete genre {id} because it has associated movies")
            deleted = genres.pop(idx)
            _write_genres(genres)
            return deleted
    return None
