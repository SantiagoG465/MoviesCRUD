import csv
import os
from typing import Optional
from models import Director, DirectorBase, DirectorUpdate

DIRECTORS_CSV = os.path.join(os.path.dirname(__file__), "data", "directors.csv")


def _parse_bool(val: str | bool) -> bool:
    if isinstance(val, bool):
        return val
    return str(val).strip().lower() in ("true", "1", "yes")


def _read_directors() -> list[Director]:
    if not os.path.exists(DIRECTORS_CSV):
        return []
    directors = []
    with open(DIRECTORS_CSV, mode="r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if not row or not row.get("id"):
                continue
            directors.append(
                Director(
                    id=int(row["id"]),
                    name=row["name"],
                    nationality=row["nationality"],
                    is_active=_parse_bool(row["is_active"]),
                )
            )
    return directors


def _write_directors(directors: list[Director]) -> None:
    os.makedirs(os.path.dirname(DIRECTORS_CSV), exist_ok=True)
    with open(DIRECTORS_CSV, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file, fieldnames=["name", "nationality", "is_active", "id"]
        )
        writer.writeheader()
        for d in directors:
            writer.writerow(
                {
                    "name": d.name,
                    "nationality": d.nationality,
                    "is_active": d.is_active,
                    "id": d.id,
                }
            )


def create_director_csv(director: DirectorBase) -> Director:
    directors = _read_directors()
    for d in directors:
        if d.name.strip().lower() == director.name.strip().lower():
            raise ValueError(f"Director '{director.name}' already exists")
    next_id = max((d.id for d in directors if d.id is not None), default=0) + 1
    new_director = Director(
        id=next_id,
        name=director.name,
        nationality=director.nationality,
        is_active=director.is_active,
    )
    directors.append(new_director)
    _write_directors(directors)
    return new_director


def show_all_directors_csv() -> list[Director]:
    return _read_directors()


def show_active_directors_csv() -> list[Director]:
    directors = _read_directors()
    return [d for d in directors if d.is_active]


def show_inactive_directors_csv() -> list[Director]:
    directors = _read_directors()
    return [d for d in directors if not d.is_active]


def find_one_director_csv(id: int) -> Optional[Director]:
    directors = _read_directors()
    for d in directors:
        if d.id == id:
            return d
    return None


def find_director_by_name_csv(name: str) -> Optional[Director]:
    directors = _read_directors()
    for d in directors:
        if name.strip().lower() in d.name.strip().lower():
            return d
    return None


def update_one_director_csv(id: int, director_update: DirectorUpdate) -> Optional[Director]:
    directors = _read_directors()
    for idx, d in enumerate(directors):
        if d.id == id:
            update_data = director_update.model_dump(exclude_unset=True)
            if "name" in update_data and update_data["name"] is not None:
                for other in directors:
                    if other.id != id and other.name.strip().lower() == update_data["name"].strip().lower():
                        raise ValueError(f"Director '{update_data['name']}' already exists")
            for key, value in update_data.items():
                if value is not None:
                    setattr(d, key, value)
            directors[idx] = d
            _write_directors(directors)
            return d
    return None


def deactivate_director_csv(id: int) -> Optional[Director]:
    directors = _read_directors()
    for idx, d in enumerate(directors):
        if d.id == id:
            d.is_active = False
            directors[idx] = d
            _write_directors(directors)
            return d
    return None
