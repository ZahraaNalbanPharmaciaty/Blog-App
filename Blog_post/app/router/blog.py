from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.operations import auth, crud
from app.schemas import blog, users



router = APIRouter(tags=['Posts'])

#get create post
@router.post("/api/posts", response_model= blog.Post)
def create_posts(title: str, description: str, tags:str,  db: Session = Depends(get_db),current_user: users.User = Depends(auth.get_current_active_user)):
    """
        Create user post

        Args: 
            post(schemas.PostCreate) : data to create post
            db: database session
            current_user: current autheticated user
        
        Return:
            Created post of schemas.Post structure
    """
    return crud.create_posts(db, title=title, description=description, tags=tags, current_user=current_user)

#get all posts
@router.get("/api/posts", response_model = list[blog.PostDetails])
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
@router.get("/api/posts/{tag}", response_model = list[blog.Post])
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

#delete posts by user
@router.delete("/api/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: users.User = Depends(auth.get_current_active_user)):
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
@router.put("/api/post/{id}", response_model= blog.Post)
def update_post(id: int, title: str = "", description: str = "", tags: str = "", db: Session = Depends(get_db), current_user: users.User = Depends(auth.get_current_active_user)):
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