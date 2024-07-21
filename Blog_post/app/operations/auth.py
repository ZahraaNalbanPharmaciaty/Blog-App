from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User
from app.schemas import auth, users

SECRET_KEY = "1e1b1550494c3c770c8c70983c0c01ff6428fc1aa40077ec6920615"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 #Authorization Token validity set to 30 minutes
USER_LOGGED_IN = False

oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "api/auth/token") #Authorization token

#Verify Password
def verify_password(user_password, password):
    """
        Verifying password entered by the user
    """
    return user_password==password

#Check if User Exists
def get_user(db: Session, username: str):
    """
        Check if user exists in database and returns user password
    """
    return db.query(User).filter(User.username == username).first()
    
#User Authentication
def authenticate_user(db, username: str, password: str):
    """
        Validates user authentication,
        if user does not exist or if there is a password mismatch return false
        if credentials meet uuser details are returned
    """
    user = get_user(db=db, username=username)
    print(user.password)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

#Creating Authoriation Token 
def create_access_token(data:dict, expires_delta: timedelta | None= None):
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
async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
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
        token_data = auth.TokenData(username=username)

    except JWTError:
        #if error is generated while decoding data, 401 Unauthorized exception is raised
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
    
    user = get_user(db=db, username=token_data.username)
    print(user)
    if user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
    return user

#Get current user details
async def get_current_active_user(current_user: users.UserInDB = Depends(get_current_user)):
    """
        Get current user details and check if the user is active
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user