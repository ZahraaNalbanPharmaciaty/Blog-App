from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User
from app.operations import auth 


router = APIRouter(tags=['Authentication'])

@router.post("/api/auth/token")
async def login_for_access(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """
        Authenticate user and generate token

        Args:
            db: database session
            form_data: form accepting username and password

        Returns:
            Token with token type
    """
    user = auth.authenticate_user(db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code = 401, detail="Incorrect username or password" ,headers={"WWW-Authenticate":"Bearer"})
    
    #Generate token with expiration time
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub":user.username}, expires_delta=access_token_expires)

    #Return access token and token type 
    return {"access_token":access_token, "token_type":"bearer"}