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
    return {"message": "Welcome to Movies API"}

