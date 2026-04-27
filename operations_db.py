from sqlmodel import Session, select
from models import Movie, MovieBase, MovieUpdate

def create_movie_db(movie: MovieBase, session: Session):
    db_movie = Movie.model_validate(movie)
    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)
    return db_movie

def show_all_movies_db(session: Session):
    return session.exec(select(Movie)).all()


def find_one_movie_db(id: int, session: Session):
    return session.get(Movie, id)


def update_one_movie_db(id: int, movie: MovieUpdate, session: Session):
    db_movie = session.get(Movie, id)
    if not db_movie:
        return None
    movie_data = movie.model_dump(exclude_unset=True)
    db_movie.sqlmodel_update(movie_data)
    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)
    return db_movie

def kill_one_movie_db(id: int, session: Session):
    db_movie = session.get(Movie, id)
    if not db_movie:
        return None
    session.delete(db_movie)
    session.commit()
    return db_movie

def filter_movies_by_genre_db(genre_id: int, session: Session):
    return session.exec(select(Movie).where(Movie.genre_id == genre_id)).all()