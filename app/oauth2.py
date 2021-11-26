from jose import JWTError, jwt
from datetime import datetime, timedelta

from . import schemas, database, models
from sqlalchemy.orm import Session

from .config import settings

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer                  # This is a schema?


# to get a string like this run:
# openssl rand -hex 32

#We have moved these into an .env file, and read this from settings
#SECRET_KEY = "Jingalala Ho!"
#ALGORITHM = "HS256"
#ACCESS_TOKEN_EXPIRE_MINUTES = 30             # standard = 30 min, testing for 1 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')              # This is getting a bit mysterious.


def create_access_token(data: dict):                                # This is the payload
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):             # Credential_exception is the exception to return, if any
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        
        # ok. So we got id. And, well, the following provides for any extensions and its validation in the future...
        token_data = schemas.TokenData(id=id)                               # What the heck is that? Look, we need to ensure tha teverything is in sync and validate

    except JWTError:                                                    # The first instance of error handling in the code?!
        raise credentials_exception

    # Note: do we return nothing?!!! Yes, we do not want to return anything per se, but we need to check for exceptions, if any
    return token_data

#This function will get called in every path, wherever we need to authenticate the user using the token....
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token_data.id).first()

    return user