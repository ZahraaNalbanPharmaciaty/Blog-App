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

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str or None = None

class User(BaseModel):
    username: str
    email: str or None = None
    full_name: str or None = None
    disabled: bool or None = None
    password: str

class UserCreate(User):
    pass

class UserInDB(User):
    password: str
