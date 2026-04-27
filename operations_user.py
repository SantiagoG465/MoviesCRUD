from sqlmodel import Session, select
from models import User, UserBase, UserUpdate


def create_user_db(user: UserBase, session: Session):
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def show_all_users_db(session: Session):
    return session.exec(select(User)).all()


def show_active_users_db(session: Session):
    return session.exec(select(User).where(User.is_active == True)).all()


def find_one_user_db(id: int, session: Session):
    return session.get(User, id)


def find_user_by_email_db(email: str, session: Session):
    return session.exec(select(User).where(User.email == email)).first()


def update_one_user_db(id: int, user: UserUpdate, session: Session):
    db_user = session.get(User, id)
    if not db_user:
        return None
    user_data = user.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
from sqlmodel import Session, select
from models import User, UserBase, UserUpdate


def create_user_db(user: UserBase, session: Session):
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def show_all_users_db(session: Session):
    return session.exec(select(User)).all()


def show_active_users_db(session: Session):
    return session.exec(select(User).where(User.is_active == True)).all()


def find_one_user_db(id: int, session: Session):
    return session.get(User, id)


def find_user_by_email_db(email: str, session: Session):
    return session.exec(select(User).where(User.email == email)).first()


def update_one_user_db(id: int, user: UserUpdate, session: Session):
    db_user = session.get(User, id)
    if not db_user:
        return None
    user_data = user.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def deactivate_user_db(id: int, session: Session):
    db_user = session.get(User, id)
    if not db_user:
        return None
    db_user.is_active = False
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
