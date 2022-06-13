import fastapi as _fastapi
import sqlalchemy.orm as _orm
import services as _services
import schemas as _schemas

app = _fastapi.FastAPI()

_services.create_database()


@app.post("/users/", response_model=_schemas.User)
def create_user(user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_user = _services.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise _fastapi.HTTPException(
            status_code=400, detail="Woops! The email is in use")

    return _services.create_user(db=db, user=user)
