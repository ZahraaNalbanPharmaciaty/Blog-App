from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    description: str
    tags: str

class PostCreate(PostBase):
    pass

class PostDetails(PostBase):
    author: str
    id: int
    URL: str
    
    class Config:
        orm_mode = True

        
class Post(PostBase):
    id: int
    
    class Config:
        orm_mode = True