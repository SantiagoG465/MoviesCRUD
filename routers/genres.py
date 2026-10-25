from fastapi import APIRouter, HTTPException
from models import GenreBase, Genre, GenreUpdate
from operations_genre_csv import (
    create_genre_csv,
    show_all_genres_csv,
    find_one_genre_csv,
    update_one_genre_csv,
    delete_one_genre_csv,
)

router = APIRouter(prefix="/genres", tags=["Genres"])


@router.post("", response_model=Genre)
async def create_genre(genre: GenreBase):
    try:
        return create_genre_csv(genre)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[Genre])
async def show_genres():
    return show_all_genres_csv()


@router.get("/{id}", response_model=Genre)
async def show_one_genre(id: int):
    genre = find_one_genre_csv(id)
    if not genre:
        raise HTTPException(status_code=404, detail=f"Genre {id} not found")
    return genre


@router.patch("/{id}", response_model=Genre)
async def update_genre(id: int, genre: GenreUpdate):
    try:
        updated = update_one_genre_csv(id, genre)
        if not updated:
            raise HTTPException(status_code=404, detail=f"Genre {id} not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{id}", response_model=Genre)
async def delete_genre(id: int):
    try:
        deleted = delete_one_genre_csv(id)
        if not deleted:
            raise HTTPException(status_code=404, detail=f"Genre {id} not found")
        return deleted
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
