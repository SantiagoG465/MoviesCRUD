from sqlmodel import Session, select
from models import Genre, GenreBase, GenreUpdate


def create_genre_db(genre: GenreBase, session: Session):
    db_genre = Genre.model_validate(genre)
    session.add(db_genre)
    session.commit()
    session.refresh(db_genre)
    return db_genre


def show_all_genres_db(session: Session):
    return session.exec(select(Genre)).all()


def find_one_genre_db(id: int, session: Session):
    return session.get(Genre, id)


def update_one_genre_db(id: int, genre: GenreUpdate, session: Session):
    db_genre = session.get(Genre, id)
    if not db_genre:
        return None
    genre_data = genre.model_dump(exclude_unset=True)
    db_genre.sqlmodel_update(genre_data)
    session.add(db_genre)
    session.commit()
    session.refresh(db_genre)
    return db_genre


def delete_one_genre_db(id: int, session: Session):
    db_genre = session.get(Genre, id)
    if not db_genre:
        return None
    session.delete(db_genre)
    session.commit()
    return db_genre