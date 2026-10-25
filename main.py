from fastapi import FastAPI
from routers import genres, movies, directors

app = FastAPI(title="MoviesCRUD API")

app.include_router(genres.router)
app.include_router(movies.router)
app.include_router(directors.router)


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to Movies API 🎬"}
