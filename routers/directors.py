from fastapi import APIRouter, HTTPException
from models import DirectorBase, Director, DirectorUpdate
from operations_director_csv import (
    create_director_csv,
    show_all_directors_csv,
    show_active_directors_csv,
    show_inactive_directors_csv,
    find_one_director_csv,
    find_director_by_name_csv,
    update_one_director_csv,
    deactivate_director_csv,
)

router = APIRouter(prefix="/directors", tags=["Directors"])


@router.post("", response_model=Director)
async def create_director(director: DirectorBase):
    try:
        return create_director_csv(director)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[Director])
async def show_directors():
    return show_all_directors_csv()


@router.get("/active", response_model=list[Director])
async def show_active_directors():
    return show_active_directors_csv()


@router.get("/inactive", response_model=list[Director])
async def show_inactive_directors():
    return show_inactive_directors_csv()


@router.get("/search", response_model=Director)
async def search_director_by_name(name: str):
    director = find_director_by_name_csv(name)
    if not director:
        raise HTTPException(status_code=404, detail=f"Director with name '{name}' not found")
    return director


@router.get("/{id}", response_model=Director)
async def show_one_director(id: int):
    director = find_one_director_csv(id)
    if not director:
        raise HTTPException(status_code=404, detail=f"Director {id} not found")
    return director


@router.patch("/{id}", response_model=Director)
async def update_director(id: int, director: DirectorUpdate):
    try:
        updated = update_one_director_csv(id, director)
        if not updated:
            raise HTTPException(status_code=404, detail=f"Director {id} not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{id}", response_model=Director)
async def deactivate_director(id: int):
    deactivated = deactivate_director_csv(id)
    if not deactivated:
        raise HTTPException(status_code=404, detail=f"Director {id} not found")
    return deactivated
