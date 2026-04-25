from fastapi import FastAPI, HTTPException
from models import MovieBase, Movie, MovieUpdate, ReviewBase, Review, ReviewUpdate
from db import SessionDep, create_all_tables
from operations_db import (create_movie_db,
                           show_all_movies_db,
                           find_one_movie_db,
                           update_one_movie_db,
                           kill_one_movie_db)
from operations_review import (create_review_db,
                                show_all_reviews_db,
                                find_one_review_db,
                                update_one_review_db,
                                deactivate_review_db,
                                show_active_reviews_db)

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


@app.post("/reviews", response_model=Review)
async def create_review(review: ReviewBase, session: SessionDep):
    return create_review_db(review, session)


@app.get("/reviews", response_model=list[Review])
async def show_reviews(session: SessionDep):
    return show_all_reviews_db(session)


@app.get("/reviews/active", response_model=list[Review])
async def show_active_reviews(session: SessionDep):
    return show_active_reviews_db(session)


@app.get("/reviews/{id}", response_model=Review)
async def show_one_review(id: int, session: SessionDep):
    review = find_one_review_db(id, session)
    if not review:
        raise HTTPException(status_code=404, detail=f"Review {id} not found")
    return review


@app.patch("/reviews/{id}", response_model=Review)
async def update_review(id: int, review: ReviewUpdate, session: SessionDep):
    updated = update_one_review_db(id, review, session)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Review {id} not found")
    return updated


@app.delete("/reviews/{id}", response_model=Review)
async def deactivate_review(id: int, session: SessionDep):
    deactivated = deactivate_review_db(id, session)
    if not deactivated:
        raise HTTPException(status_code=404, detail=f"Review {id} not found")
    return deactivated