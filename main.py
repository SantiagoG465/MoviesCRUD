from fastapi import FastAPI, HTTPException
from models import (
    MovieBase,
    Movie,
    MovieUpdate,
    GenreBase,
    Genre,
    GenreUpdate,
    DirectorBase,
    Director,
    DirectorUpdate,
)

from operations_movie_csv import (
    create_movie_csv,
    show_all_movies_csv,
    find_one_movie_csv,
    update_one_movie_csv,
    kill_one_movie_csv,
    filter_movies_by_genre_csv,
)

from operations_genre_csv import (
    create_genre_csv,
    show_all_genres_csv,
    find_one_genre_csv,
    update_one_genre_csv,
    delete_one_genre_csv,
)

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

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to Movies API 🎬"}


@app.post("/genres", response_model=Genre)
async def create_genre(genre: GenreBase):
    try:
        return create_genre_csv(genre)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/genres", response_model=list[Genre])
async def show_genres():
    return show_all_genres_csv()


@app.get("/genres/{id}", response_model=Genre)
async def show_one_genre(id: int):
    genre = find_one_genre_csv(id)
    if not genre:
        raise HTTPException(status_code=404, detail=f"Genre {id} not found")
    return genre


@app.patch("/genres/{id}", response_model=Genre)
async def update_genre(id: int, genre: GenreUpdate):
    try:
        updated = update_one_genre_csv(id, genre)
        if not updated:
            raise HTTPException(status_code=404, detail=f"Genre {id} not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/genres/{id}", response_model=Genre)
async def delete_genre(id: int):
    try:
        deleted = delete_one_genre_csv(id)
        if not deleted:
            raise HTTPException(status_code=404, detail=f"Genre {id} not found")
        return deleted
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/movies", response_model=Movie)
async def create_movie(movie: MovieBase):
    try:
        return create_movie_csv(movie)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/movies", response_model=list[Movie])
async def show_movies():
    return show_all_movies_csv()


@app.get("/movies/filter", response_model=list[Movie])
async def filter_movies_by_genre(genre_id: int):
    movies = filter_movies_by_genre_csv(genre_id)
    if not movies:
        raise HTTPException(status_code=404, detail=f"No movies found for genre {genre_id}")
    return movies


@app.get("/movies/{id}", response_model=Movie)
async def show_one_movie(id: int):
    movie = find_one_movie_csv(id)
    if not movie:
        raise HTTPException(status_code=404, detail=f"Movie {id} not found")
    return movie


@app.patch("/movies/{id}", response_model=Movie)
async def update_movie(id: int, movie: MovieUpdate):
    try:
        updated = update_one_movie_csv(id, movie)
        if not updated:
            raise HTTPException(status_code=404, detail=f"Movie {id} not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/movies/{id}", response_model=Movie)
async def delete_movie(id: int):
    deleted = kill_one_movie_csv(id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Movie {id} not found")
    return deleted


@app.post("/directors", response_model=Director)
async def create_director(director: DirectorBase):
    try:
        return create_director_csv(director)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/directors", response_model=list[Director])
async def show_directors():
    return show_all_directors_csv()


@app.get("/directors/active", response_model=list[Director])
async def show_active_directors():
    return show_active_directors_csv()


@app.get("/directors/inactive", response_model=list[Director])
async def show_inactive_directors():
    return show_inactive_directors_csv()


@app.get("/directors/search", response_model=Director)
async def search_director_by_name(name: str):
    director = find_director_by_name_csv(name)
    if not director:
        raise HTTPException(status_code=404, detail=f"Director with name '{name}' not found")
    return director


@app.get("/directors/{id}", response_model=Director)
async def show_one_director(id: int):
    director = find_one_director_csv(id)
    if not director:
        raise HTTPException(status_code=404, detail=f"Director {id} not found")
    return director


@app.patch("/directors/{id}", response_model=Director)
async def update_director(id: int, director: DirectorUpdate):
    try:
        updated = update_one_director_csv(id, director)
        if not updated:
            raise HTTPException(status_code=404, detail=f"Director {id} not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/directors/{id}", response_model=Director)
async def deactivate_director(id: int):
    deactivated = deactivate_director_csv(id)
    if not deactivated:
        raise HTTPException(status_code=404, detail=f"Director {id} not found")
    return deactivated
