from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm                   # Improvement

from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm=Depends(), db: Session= Depends(database.get_db)):      # replacing schemas.UserLogin, with OAuth2PasswordForm

    # Note OAuth2PasswordRequestForm returns the user_credentials as a dict ==> {"username": "blah", "password":" blah"}
    # So we cannot use user_credentials.email, but now user_credentials.username

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials1")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials2")

    # create a token: What is the data that we want to encode? This is our decision. We want only user_id for the time being
    access_token = oauth2.create_access_token({"user_id": user.id})

    # return token
    return {"access_token": access_token, "token_type": "Bearer"}
