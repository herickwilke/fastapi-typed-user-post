import sqlalchemy.orm as _orm
import database as _database
import models as _models
import schemas as _schemas


def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_by_email(db: _orm.Session, email: str):
    return db.query(_models.User).filter(_models.User.email == email).first()


def create_user(db: _orm.Session, user: _schemas.UserCreate):
    faked_hashed_password = user.password = "thisisnotsecure"
    db_user = _models.User(
        email=user.email, hashed_password=faked_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
