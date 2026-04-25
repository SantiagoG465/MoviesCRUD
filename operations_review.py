from sqlmodel import Session, select
from models import Review, ReviewBase, ReviewUpdate


def create_review_db(review: ReviewBase, session: Session):
    db_review = Review.model_validate(review)
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review


def show_all_reviews_db(session: Session):
    return session.exec(select(Review)).all()


def find_one_review_db(id: int, session: Session):
    return session.get(Review, id)


def update_one_review_db(id: int, review: ReviewUpdate, session: Session):
    db_review = session.get(Review, id)
    if not db_review:
        return None
    review_data = review.model_dump(exclude_unset=True)
    db_review.sqlmodel_update(review_data)
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review


def deactivate_review_db(id: int, session: Session):
    db_review = session.get(Review, id)
    if not db_review:
        return None
    db_review.is_active = False
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review


def show_active_reviews_db(session: Session):
    return session.exec(select(Review).where(Review.is_active == True)).all()