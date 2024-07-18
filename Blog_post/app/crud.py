from sqlalchemy.orm import Session
from . import models, schemas, utils, auth

#Get active posts from database
def get_posts(db: Session):
    return db.query(models.Posts).filter(models.Posts.deleted == False).all()

#Create posts 
def create_posts(db: Session, post: schemas.PostCreate, current_user: dict):
    db_post = models.Posts(title=post.title, description=post.description, tags=post.tags, URL=utils.convert_title_to_url(post.title), author=current_user.username)
    db.add(db_post)
    db.commit()
    return db_post

#Get active posts by author
def get_posts_by_author(db: Session, current_user: dict):
    return db.query(models.Posts).filter(models.Posts.author == current_user.username, models.Posts.deleted == False).all()

#Delete posts by author based on id
def delete_post(db: Session, id:int, current_user: dict):
    db_post = db.query(models.Posts).filter(models.Posts.id == id,models.Posts.author == current_user).first()
    if db_post:
        db_post.deleted = True
        db.commit()
    return db_post

#Update posts by author
def update_post(db: Session, id: int, current_user: dict, post: schemas.PostCreate,):
    db_post = db.query(models.Posts).filter(models.Posts.id == id,models.Posts.author == current_user).first()
    if db_post:
        db_post.title = post.title
        db_post.description = post.description
        db_post.URL = utils.convert_title_to_url(db_post.title)
        db_post.tags = post.tags
        db.commit()
    return db_post

#Creating users
def create_user(user: schemas.UserCreate):
    user_db = {
        "username": user.username,
        "full_name": user.full_name,
        "email": user.email,
        "password": user.password,
        "disabled": False
    }
    print(user_db)
    auth.user_db[user.username] = user_db
    return user_db