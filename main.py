from fastapi import FastAPI, HTTPException
from models import MovieBase, Movie, MovieUpdate, GenreBase, Genre, GenreUpdate, UserBase, User, UserUpdate

from operations_movie_csv import (
    create_movie_csv,
    show_all_movies_csv,
    find_one_movie_csv,
    update_one_movie_csv,
    kill_one_movie_csv,
    filter_movies_by_genre_csv
)

from operations_genre_csv import (
    create_genre_csv,
    show_all_genres_csv,
    find_one_genre_csv,
    update_one_genre_csv,
    delete_one_genre_csv
)

from operations_user_csv import (
    create_user_csv,
    show_all_users_csv,
    show_active_users_csv,
    find_one_user_csv,
    find_user_by_email_csv,
    update_one_user_csv,
    deactivate_user_csv
)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to Movies API 🎬"}


@app.post("/genres", response_model=Genre)
async def create_genre(genre: GenreBase):
    return create_genre_csv(genre)


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
    updated = update_one_genre_csv(id, genre)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Genre {id} not found")
    return updated


@app.delete("/genres/{id}", response_model=Genre)
async def delete_genre(id: int):
    deleted = delete_one_genre_csv(id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Genre {id} not found")
    return deleted


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

@app.post("/users", response_model=User)
async def create_user(user: UserBase):
    return create_user_csv(user)


@app.get("/users", response_model=list[User])
async def show_users():
    return show_all_users_csv()


@app.get("/users/active", response_model=list[User])
async def show_active_users():
    return show_active_users_csv()


@app.get("/users/search", response_model=User)
async def search_user_by_email(email: str):
    user = find_user_by_email_csv(email)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with email {email} not found")
    return user


@app.get("/users/{id}", response_model=User)
async def show_one_user(id: int):
    user = find_one_user_csv(id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {id} not found")
    return user


@app.patch("/users/{id}", response_model=User)
async def update_user(id: int, user: UserUpdate):
    updated = update_one_user_csv(id, user)
    if not updated:
        raise HTTPException(status_code=404, detail=f"User {id} not found")
    return updated


@app.delete("/users/{id}", response_model=User)
async def deactivate_user(id: int):
    deactivated = deactivate_user_csv(id)
    if not deactivated:
        raise HTTPException(status_code=404, detail=f"User {id} not found")
    return deactivated