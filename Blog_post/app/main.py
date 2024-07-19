"""
********************************************************************

BLOG APPLICATION USING FASTAPI
Author: Zahraa Nalban

********************************************************************
"""

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session # type: ignore
from .database import get_db, init_db
from . import schemas, crud, auth
from fastapi.security import OAuth2PasswordRequestForm # type: ignore
from datetime import timedelta
from typing import Optional

app = FastAPI()

#On application startup
@app.on_event("startup")
def application_startup():
    # Attempt database initialisation on application startup
    init_db()

#token generation for login
@app.post("/token", response_model = schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm=Depends()):
    # Authenticate user using credentials from form_data
    user = auth.authenticate_user(auth.user_db, form_data.username, form_data.password)

    # If authentication fails, raise HTTP 401 Exception
    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password" ,header={"WWW-Authenticate":"Bearer"})
    
    #Generate token with expiration time
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub":user.username}, expires_delta=access_token_expires)

    #Return access token and token type 
    return {"access_token":access_token, "token_type":"bearer"}

# get logged in user details
@app.get("/users/me/")
async def read_users_me(current_user: schemas.User = Depends(auth.get_current_active_user)):
    return current_user

#get create post
@app.post("/posts", response_model= schemas.Post)
def create_posts(post: schemas.PostCreate,  db: Session = Depends(get_db),current_user: schemas.User = Depends(auth.get_current_active_user)):
    """
        Create user post

        Args: 
            post(schemas.PostCreate) : data to create post
            db: database session
            current_user: current autheticated user
        
        Return:
            Created post of schemas.Post structure
    """
    return crud.create_posts(db, post = post, current_user=current_user)

#get all posts
@app.get("/posts", response_model = list[schemas.PostDetails])
def retrieve_posts(db: Session = Depends(get_db)):
    """
        Retrieve posts from database
        
        Args:
            db: database session

        Return:
            list of posts in schemas.PostSetails structure

    """
    post = crud.get_posts(db)
    return post

#get posts based on tag
@app.get("/posts/tag/{tag}", response_model = list[schemas.Post])
def retrieve_post_by_tag(tag: str, db: Session = Depends(get_db)):
    """
        Retrive Posts by tag 

        Arg:
            tag: category of post
            db: database session
        
        Returns:
            List of posts filtered by tags in schemas.PostDetails structure

        [FIX] Search by tag is no more case sensitive
    """

    #Store filtered posts
    posts =[] 

    #For loop to check each post in the database
    for post in crud.get_posts(db):

        #Check presence of tag in post's tag
        #if the tag exists, add it to the list of filtered posts
        if tag.lower() in post.tags.lower().split(","):
            posts.append(post)

    # If no posts exist, Not found exception is generated
    if post ==[]:
        raise HTTPException(status_code=404, detail="Not found")
    return posts

#get posts by user
@app.get("/posts/me", response_model = list[schemas.PostDetails])
def retrieve_post_by_author(author: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    """
        Retrieve user's posts from database

        Args:
            author: current author
            db: database session

        Returns:
            List of posts in schemas.PostDetails structure
    """
    post = crud.get_posts_by_author(db, current_user=author)

    #if no posts exist, HTTP Exception is raised
    if post ==[]:
        raise HTTPException(status_code=404, detail="Not found")
    return post
#delete posts by user
@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_active_user)):
    """
        Deletes post based on post id

        Args:
            id: post id
            db: database session
        
        Returns:
            Deletes post and returns the deleted post as response
        
        [FIX] Only posts by users can be deleted, if the post does not belong to user, not found error will be displayed
    """
    deleted_post = crud.delete_post(db=db, id=id, current_user=current_user.username)

    #if post does not exist, Not found error will be raised
    if deleted_post == []: 
        raise HTTPException(status_code=404,detail="Not found")
    return deleted_post

#update posts
@app.put("/post/{id}", response_model= schemas.Post)
def update_post(id: int, title: str = "", description: str = "", tags: str = "", db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_active_user)):
    """
        Update post based on id

        Args:
            id: post id
            post(schemas.PostCreate) : data to update post
            db: database session 
            current_user: gets current active user details

        Returns:
            Updates post and returns the updated post
    """
    return crud.update_post(db=db, id=id, current_user=current_user.username, title=title, description=description, tags=tags)

#create user
@app.post("/users/create")
def create_user(user: schemas.UserCreate, current_user: schemas.User = Depends(auth.get_current_user)):
    """
        Creates user 
        
        Args:
            user(schemas.UserCreate): credentials and details of user to be created

        Returns:
            Creates user and returns details
    """
    
    return crud.create_user(user = user)