from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from . import schemas
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status

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
        "disabled": False
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
    """
        Check if user exists in database and returns user password
    """
    if username in db:
        user_data=db[username]
        return schemas.UserInDB(**user_data)
    
#User Authentication
def authenticate_user(db, username: str, password: str):
    """
        Validates user authentication,
        if user does not exist or if there is a password mismatch return false
        if credentials meet uuser details are returned
    """
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

#Creating Authoriation Token 
def create_access_token(data:dict, expires_delta: timedelta or None= None):
    """
        Generated authentication token on login for user authentication

        Args:
            data: data to encode token
            expires_delta: sets expiration time to token
        
        Returns:
            token generated and returned        
    """

    #Generates copy of data
    to_encode = data.copy()

    #sets expirations time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    #updates expiration time
    to_encode.update({"exp":expire})

    #generate token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#Check current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
        Decodes the token and gets user details.
        if user details are not found unauthorized error will be displayed

        Args:
            token: jwt token

        Returns:
            user details after authenticating with token
    """
    try:
        # Decodes token with secret key and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Gets username from token payload
        username: str = payload.get("sub")

        #if username not found, 401 Unauthorized exception is raised
        if username is None:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
        
        #create token_data object with username
        token_data = schemas.TokenData(username=username)

    except JWTError:
        #if error is generated while decoding data, 401 Unauthorized exception is raised
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
    
    user = get_user(user_db, username=token_data.username)
    if user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
    return user

#Get current user details
async def get_current_active_user(current_user: schemas.UserInDB = Depends(get_current_user)):
    """
        Get current user details and check if the user is active
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user