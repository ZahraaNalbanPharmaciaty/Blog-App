from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from . import schemas
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends

SECRET_KEY = "1e1b1550494c3c770c8c70983c0c01ff6428fc1aa40077ec6920615"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 #Authorization Token validity set to 30 minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "token") #Authorization token

user_db = { #User database
    "zara": {
        "username": "zara",
        "full_name": "Zahraa Nalban",
        "email": "zahraa@example.com",
        "password": "123",
        "disabled": False,
    },
    "tim": {
        "username": "tim",
        "full_name": "Tim",
        "email": "tim@example.com",
        "password": "1234",
        "disabled": False

    }
}

#Verify Password
def verify_password(user_password, password):
    return user_password==password

#Check if User Exists
def get_user(db, username: str):
    if username in db:
        user_data=db[username]
        return schemas.UserInDB(**user_data)
    
#User Authentication
def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

#Creating Authoriation Token 
def create_access_token(data:dict, expires_delta: timedelta or None= None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#Check current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
    user = get_user(user_db, username=token_data.username)
    if user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
    return user

#Get current user details
async def get_current_active_user(current_user: schemas.UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user