from typing import List
import fastapi as _fastapi
import sqlalchemy.orm as _orm
import services as _services
import schemas as _schemas

app = _fastapi.FastAPI()

_services.create_database()


@app.post("/users/", response_model=_schemas.User)
def create_user(user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    '''
    Creates a new user 
    '''
    db_user = _services.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise _fastapi.HTTPException(
            status_code=400, detail="Woops! The email is in use")

    return _services.create_user(db=db, user=user)


@app.get("/users/", response_model=List[_schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    '''
    Get all the users from the database, but paginating them. Default setted 0 to 10. 
    '''
    users = _services.get_users(db=db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=_schemas.User)
def read_user(user_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    '''
    Get a specific user from the database given an id
    '''
    db_user = _services.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="Sorry, this user doesn't exist")
    return db_user


@app.post("/users/{user_id}/posts/", response_model=_schemas.Post)
def create_post(user_id: int, post: _schemas._PostCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    '''
    Creates a new post related to a user
    '''
    db_user = _services.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="Sorry, this user doesn't exist")
    return _services.create_post(db=db, post=post, user_id=user_id)


@app.get("/posts/", response_model=List[_schemas.Post])
def read_posts(skip: int = 0, limit: int = 10, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    '''
    Get all the posts from the database, but paginating them. Default setted 0 to 10. 
    '''
    posts = _services.get_posts(db=db, skip=skip, limit=limit)
    return posts


@app.get("/posts/{post_id}", response_model=_schemas.Post)
def read_post(post_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    post = _services.get_post(db=db, post_id=post_id)
    if post is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="Sorry, this post doesn't exist")
    return post
