from fastapi import FastAPI, HTTPException
from models import MovieBase, Movie, MovieUpdate, GenreBase, Genre, GenreUpdate, UserBase, User, UserUpdate
from db import SessionDep, create_all_tables
from operations_db import (create_movie_db,
                           show_all_movies_db,
                           find_one_movie_db,
                           update_one_movie_db,
                           kill_one_movie_db,
                           filter_movies_by_genre_db)
from operations_genre import (create_genre_db,
                               show_all_genres_db,
                               find_one_genre_db,
                               update_one_genre_db,
                               delete_one_genre_db)
from operations_user import (create_user_db,
                              show_all_users_db,
                              show_active_users_db,
                              find_one_user_db,
                              find_user_by_email_db,
                              update_one_user_db,
                              deactivate_user_db)

app = FastAPI(lifespan=create_all_tables)


@app.get("/")
async def root():
    return {"message": "Welcome to Movies API 🎬"}


@app.post("/genres", response_model=Genre)
async def create_genre(genre: GenreBase, session: SessionDep):
    return create_genre_db(genre, session)


@app.get("/genres", response_model=list[Genre])
async def show_genres(session: SessionDep):
    return show_all_genres_db(session)


@app.get("/genres/{id}", response_model=Genre)
async def show_one_genre(id: int, session: SessionDep):
    genre = find_one_genre_db(id, session)
    if not genre:
        raise HTTPException(status_code=404, detail=f"Genre {id} not found")
    return genre


@app.patch("/genres/{id}", response_model=Genre)
async def update_genre(id: int, genre: GenreUpdate, session: SessionDep):
    updated = update_one_genre_db(id, genre, session)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Genre {id} not found")
    return updated


@app.delete("/genres/{id}", response_model=Genre)
async def delete_genre(id: int, session: SessionDep):
    deleted = delete_one_genre_db(id, session)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Genre {id} not found")
    return deleted


# Movie endpoints
@app.post("/movies", response_model=Movie)
async def create_movie(movie: MovieBase, session: SessionDep):
    return create_movie_db(movie, session)


@app.get("/movies", response_model=list[Movie])
async def show_movies(session: SessionDep):
    return show_all_movies_db(session)

@app.get("/movies/filter", response_model=list[Movie])
async def filter_movies_by_genre(genre_id: int, session: SessionDep):
    movies = filter_movies_by_genre_db(genre_id, session)
    if not movies:
        raise HTTPException(status_code=404, detail=f"No movies found for genre {genre_id}")
    return movies

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


# User endpoints
@app.post("/users", response_model=User)
async def create_user(user: UserBase, session: SessionDep):
    return create_user_db(user, session)


@app.get("/users", response_model=list[User])
async def show_users(session: SessionDep):
    return show_all_users_db(session)


@app.get("/users/active", response_model=list[User])
async def show_active_users(session: SessionDep):
    return show_active_users_db(session)


@app.get("/users/search", response_model=User)
async def search_user_by_email(email: str, session: SessionDep):
    user = find_user_by_email_db(email, session)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with email {email} not found")
    return user


@app.get("/users/{id}", response_model=User)
async def show_one_user(id: int, session: SessionDep):
    user = find_one_user_db(id, session)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {id} not found")
    return user


@app.patch("/users/{id}", response_model=User)
async def update_user(id: int, user: UserUpdate, session: SessionDep):
    updated = update_one_user_db(id, user, session)
    if not updated:
        raise HTTPException(status_code=404, detail=f"User {id} not found")
    return updated


@app.delete("/users/{id}", response_model=User)
async def deactivate_user(id: int, session: SessionDep):
    deactivated = deactivate_user_db(id, session)
    if not deactivated:
        raise HTTPException(status_code=404, detail=f"User {id} not found")
    return deactivated