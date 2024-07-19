from sqlalchemy.orm import Session # type: ignore
from . import models, schemas, utils, auth


#Get active posts from database
def get_posts(db: Session):
    """
        Retrieve active posts from database
    """
    return db.query(models.Posts).filter(models.Posts.deleted == False).all()

#Create posts 
def create_posts(db: Session, post: schemas.PostCreate, current_user: dict):
    """
        Create posts and update to database
    """
    db_post = models.Posts(title=post.title, description=post.description, tags=post.tags, URL=utils.convert_title_to_url(post.title), author=current_user.username)
    db.add(db_post)
    db.commit()
    return db_post

#Get active posts by author
def get_posts_by_author(db: Session, current_user: dict):
    """
        Retrive all posts by user
    """
    return db.query(models.Posts).filter(models.Posts.author == current_user.username, models.Posts.deleted == False).all()

#Delete posts by author based on id
def delete_post(db: Session, id:int, current_user: dict):
    """
        Delete post by post id
    """

    db_post = db.query(models.Posts).filter(models.Posts.id == id,models.Posts.author == current_user).all()
    if db_post:
        db_post.deleted = True
        db.commit()
    return db_post

#Update posts by author
def update_post(db: Session, id: int, current_user: dict, title: str, description: str, tags: str):
    """
        Update data post by author based on id
    """
    db_post = db.query(models.Posts).filter(models.Posts.id == id,models.Posts.author == current_user).first()
    if db_post:
        if title != "":
            db_post.title = title
            db_post.URL = utils.convert_title_to_url(db_post.title)
        if description != "":
            db_post.description = description
        if tags != "":
            db_post.tags = tags
        db.commit()
    return db_post

#Creating users
def create_user(user: schemas.UserCreate):
    """
        Create User
    """

    user_db = {
        "username": user.username,
        "full_name": user.full_name,
        "email": user.email,
        "password": user.password,
        "disabled": False
    }
    auth.user_db[user.username] = user_db
    return user_db