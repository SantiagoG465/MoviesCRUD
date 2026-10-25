import csv
import os
from typing import Optional
from models import User, UserBase, UserUpdate

USERS_CSV = os.path.join(os.path.dirname(__file__), "data", "users.csv")


def _parse_bool(val: str | bool) -> bool:
    if isinstance(val, bool):
        return val
    return str(val).strip().lower() in ("true", "1", "yes")


def _read_users() -> list[User]:
    if not os.path.exists(USERS_CSV):
        return []
    users = []
    with open(USERS_CSV, mode="r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if not row or not row.get("id"):
                continue
            users.append(
                User(
                    id=int(row["id"]),
                    name=row["name"],
                    email=row["email"],
                    is_active=_parse_bool(row["is_active"]),
                )
            )
    return users


def _write_users(users: list[User]) -> None:
    os.makedirs(os.path.dirname(USERS_CSV), exist_ok=True)
    with open(USERS_CSV, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file, fieldnames=["name", "email", "is_active", "id"]
        )
        writer.writeheader()
        for u in users:
            writer.writerow(
                {
                    "name": u.name,
                    "email": u.email,
                    "is_active": u.is_active,
                    "id": u.id,
                }
            )


def create_user_csv(user: UserBase) -> User:
    users = _read_users()
    for u in users:
        if u.email.strip().lower() == user.email.strip().lower():
            raise ValueError(f"User with email '{user.email}' already exists")
    next_id = max((u.id for u in users if u.id is not None), default=0) + 1
    new_user = User(
        id=next_id,
        name=user.name,
        email=user.email,
        is_active=user.is_active,
    )
    users.append(new_user)
    _write_users(users)
    return new_user


def show_all_users_csv() -> list[User]:
    return _read_users()


def show_active_users_csv() -> list[User]:
    users = _read_users()
    return [u for u in users if u.is_active]


def show_inactive_users_csv() -> list[User]:
    users = _read_users()
    return [u for u in users if not u.is_active]


def find_one_user_csv(id: int) -> Optional[User]:
    users = _read_users()
    for u in users:
        if u.id == id:
            return u
    return None


def find_user_by_email_csv(email: str) -> Optional[User]:
    users = _read_users()
    for u in users:
        if u.email.strip().lower() == email.strip().lower():
            return u
    return None


def update_one_user_csv(id: int, user_update: UserUpdate) -> Optional[User]:
    users = _read_users()
    for idx, u in enumerate(users):
        if u.id == id:
            update_data = user_update.model_dump(exclude_unset=True)
            if "email" in update_data and update_data["email"] is not None:
                for other in users:
                    if other.id != id and other.email.strip().lower() == update_data["email"].strip().lower():
                        raise ValueError(f"User with email '{update_data['email']}' already exists")
            for key, value in update_data.items():
                if value is not None:
                    setattr(u, key, value)
            users[idx] = u
            _write_users(users)
            return u
    return None


def deactivate_user_csv(id: int) -> Optional[User]:
    users = _read_users()
    for idx, u in enumerate(users):
        if u.id == id:
            u.is_active = False
            users[idx] = u
            _write_users(users)
            return u
    return None
