from starlette.exceptions import HTTPException
from sqlalchemy.orm import Session
from app.models.models import Posts, User
from app.utils import convert_title_to_url
from starlette.responses import Response

#Create user
def create_user(db: Session, username: str, full_name: str, password: str, email: str):
    """
        Create user and update database
    """
    check_user = db.query(User).filter(User.username == username).first()
    if check_user:
        raise HTTPException(status_code=409, detail="User already Exists, Please choose a different username")
    db_user = User(username=username, full_name=full_name, password=password, email=email, disabled=False)
    db.add(db_user)
    db.commit()
    return {
        "msg": "User created"
    }


#Get active posts from database
def get_posts(db: Session):
    """
        Retrieve active posts from database
    """
    return db.query(Posts).filter(Posts.deleted == False).all()


#Create posts 
def create_posts(db: Session, title:str, description: str, tags:str, current_user: dict):
    """
        Create posts and update to database
    """
    db_post = Posts(title=title, description=description, tags=tags, URL=convert_title_to_url(title), author=current_user.username)
    db.add(db_post)
    db.commit()
    return db_post


#Get active posts by author
def get_posts_by_author(db: Session, current_user: dict):
    """
        Retrive all posts by user
    """
    return db.query(Posts).filter(Posts.author == current_user.username, Posts.deleted == False).all()

#Delete posts by author based on id
def delete_post(db: Session, id:int, current_user: str):
    """
        Delete post by post id
    """

    db_post = db.query(Posts).filter(Posts.id == id,Posts.author == current_user).first()

    if not db_post:
        raise HTTPException(status_code=404, detail="Not found")
    if db_post.deleted:
        raise HTTPException(status_code=405, detail="Already deleted")
    db_post.deleted = True
    db.commit()
    return db_post


#Delete posts by author based on id
def delete_user(db: Session, id:int, current_user: str):
    """
        Delete post by post id
    """

    db_user = db.query(User).filter(User.id == id, User.username == current_user).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="Not found")
    if db_user.disabled:
        raise HTTPException(status_code=405, detail="Already deleted")
    db_user.disabled = True
    db.commit()
    return db_user

#Update posts by author
def update_post(db: Session, id: int, current_user: dict, title: str, description: str, tags: str):
    """
        Update data post by author based on id
    """
    db_post = db.query(Posts).filter(Posts.id == id, Posts.author == current_user, Posts.deleted ==False).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Not found")
    if title != "":
        db_post.title = title
        db_post.URL = convert_title_to_url(db_post.title)
    if description != "":
        db_post.description = description
    if tags != "":
        db_post.tags = tags
    db.commit()
    return db_post




