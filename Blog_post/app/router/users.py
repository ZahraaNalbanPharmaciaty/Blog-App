from fastapi import APIRouter, Depends, Form, HTTPException
from pytest import Session
from app.database import get_db
from app.operations import auth, crud
from app.schemas import blog, users
router = APIRouter(tags=["Users"])

@router.post("/api/users/create")
async def create_user(username: str = Form(...), email: str = Form(...), password: str = Form(...), full_name: str = Form(...), db: Session = Depends(get_db)):
    """
        Create user

        Args:
            username: new users username
            email: new users email
            password: new users password
            full_name: new users name
            db: database session
        
        Return:
            User created
    """
    return crud.create_user(db=db, username=username, password=password, email=email, full_name=full_name)

@router.get("/api/users/me/")
async def read_users_me(current_user: users.User = Depends(auth.get_current_active_user)):
    """
        Retrive user details

        Args:
            current_user: get current user
        
        Returns:
            User details
    """
    return current_user

#get posts by user
@router.get("/api/users/posts", response_model = list[blog.PostDetails])
def retrieve_post_by_author(author: users.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    """
        Retrieve user's posts from database

        Args:
            author: current author
            db: database session

        Returns:
            List of posts in schemas.PostDetails structure
    """
    print(author.username)
    post = crud.get_posts_by_author(db, current_user=author)

    #if no posts exist, HTTP Exception is raised
    if post ==[]:
        raise HTTPException(status_code=404, detail="Not found")
    return post