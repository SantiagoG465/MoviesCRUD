from fastapi import APIRouter, HTTPException
from models import MovieBase, Movie, MovieUpdate
from operations_movie_csv import (
    create_movie_csv,
    show_all_movies_csv,
    find_one_movie_csv,
    update_one_movie_csv,
    kill_one_movie_csv,
    filter_movies_by_genre_csv,
)

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.post("", response_model=Movie)
async def create_movie(movie: MovieBase):
    try:
        return create_movie_csv(movie)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[Movie])
async def show_movies():
    return show_all_movies_csv()


@router.get("/filter", response_model=list[Movie])
async def filter_movies_by_genre(genre_id: int):
    movies = filter_movies_by_genre_csv(genre_id)
    if not movies:
        raise HTTPException(status_code=404, detail=f"No movies found for genre {genre_id}")
    return movies


@router.get("/{id}", response_model=Movie)
async def show_one_movie(id: int):
    movie = find_one_movie_csv(id)
    if not movie:
        raise HTTPException(status_code=404, detail=f"Movie {id} not found")
    return movie


@router.patch("/{id}", response_model=Movie)
async def update_movie(id: int, movie: MovieUpdate):
    try:
        updated = update_one_movie_csv(id, movie)
        if not updated:
            raise HTTPException(status_code=404, detail=f"Movie {id} not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{id}", response_model=Movie)
async def delete_movie(id: int):
    deleted = kill_one_movie_csv(id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Movie {id} not found")
    return deleted
