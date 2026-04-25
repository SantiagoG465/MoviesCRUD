from fastapi import FastAPI, HTTPException
from models import MovieBase, Movie, MovieUpdate
from db import SessionDep, create_all_tables
from operations_db import (create_movie_db,
                           show_all_movies_db,
                           find_one_movie_db,
                           update_one_movie_db,
                           kill_one_movie_db)

app = FastAPI(lifespan=create_all_tables)


@app.get("/")
async def root():
    return {"message": "Welcome to Movies API 🎬"}


@app.post("/movies", response_model=Movie)
async def create_movie(movie: MovieBase, session: SessionDep):
    return create_movie_db(movie, session)


@app.get("/movies", response_model=list[Movie])
async def show_movies(session: SessionDep):
    return show_all_movies_db(session)


@app.get("/movies/{id}", response_model=Movie)
async def show_one_movie(id: int, session: SessionDep):
    movie = find_one_movie_db(id, session)
    if not movie:
        raise HTTPException(status_code=404, detail=f"Movie {id} not found")
    return movie


@app.patch("/movies/{id}", response_model=Movie)
async def update_movie(id: int, movie: MovieUpdate, session: SessionDep):
    updated = update_one_movie_db(id, movie, session)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Movie {id} not found")
    return updated


@app.delete("/movies/{id}", response_model=Movie)
async def delete_movie(id: int, session: SessionDep):
    deleted = kill_one_movie_db(id, session)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Movie {id} not found")
    return deleted