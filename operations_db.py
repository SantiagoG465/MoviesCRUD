from sqlalchemy import Session, select
from models import Movie, MovieBase, MovieUpdate

def create_movie(movie: MovieBase, session: Session):
    db_movie = Movie.model_validate(movie)
    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)
    return db_movie