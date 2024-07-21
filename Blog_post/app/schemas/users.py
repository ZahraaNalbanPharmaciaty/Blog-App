from pydantic import BaseModel, EmailStr

class User(BaseModel):
    username: str
    email: EmailStr | None = None
    full_name: str | None = None
    disabled: bool | None = None
    password: str | None

class UserCreate(User):
    pass

class UserInDB(User):
    password: str