'''
********************************************************************

BLOG APPLICATION USING FASTAPI
Author: Zahraa Nalban

********************************************************************
'''

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session # type: ignore
from .database import get_db, init_db
from . import schemas, crud, auth
from fastapi.security import OAuth2PasswordRequestForm # type: ignore
from datetime import timedelta

app = FastAPI()

#On application startup
@app.on_event("startup")
def application_startup():
    init_db()

#token generation for login
@app.post("/token", response_model = schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm=Depends()):
    user = auth.authenticate_user(auth.user_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password" ,header={"WWW-Authenticate":"Bearer"})
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub":user.username}, expires_delta=access_token_expires)
    return {"access_token":access_token, "token_type":"bearer"}

# get logged in user details
@app.get("/users/me/")
async def read_users_me(current_user: schemas.User = Depends(auth.get_current_active_user)):
    return current_user

#get create post
@app.post("/posts", response_model= schemas.Post)
def create_posts(post: schemas.PostCreate,  db: Session = Depends(get_db),current_user: schemas.User = Depends(auth.get_current_active_user)):
    return crud.create_posts(db, post = post, current_user=current_user)

#get all posts
@app.get("/posts", response_model = list[schemas.PostDetails])
def retrieve_posts(db: Session = Depends(get_db)):
    post = crud.get_posts(db)
    return post

#get posts by user
@app.get("/posts/me", response_model = list[schemas.PostDetails])
def retrieve_post_by_author(author: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    post = crud.get_posts_by_author(db, current_user=author)
    if post ==[]:
        raise HTTPException(status_code=404, detail="Not found")
    return post

#get posts based on tag
@app.get("/posts/tag/{tag}", response_model = list[schemas.Post])
def retrieve_post_by_tag(tag: str, db: Session = Depends(get_db)):
    posts =[] 
    for post in crud.get_posts(db):
        if tag in post.tags.split(","):
            posts.append(post)
    if post ==[]:
        raise HTTPException(status_code=404, detail="Not found")
    return posts

#delete posts by user
@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_active_user)):
    return crud.delete_post(db=db, id=id, current_user=current_user.username)

#update posts
@app.put("/post/{id}", response_model= schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_active_user)):
    return crud.update_post(db=db, id=id, current_user=current_user.username, post=post)

#create user
@app.post("/users/create")
def create_user(user: schemas.UserCreate):
    return crud.create_user(user = user)