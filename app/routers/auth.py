from fastapi import APIRouter, Depends, Response, status, HTTPException
from requests import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models
from .. import database, schemas, utils, oauth2

router = APIRouter(tags=["Authentication"])


@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()  # will check if the email exists
    # credentials will have username and password variables only due to OAuth2PasswordRequestForm

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    # checks the entered password with the hash password
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    # creating an access token
    access_token = oauth2.create_access_token(
        data={"user_id": user.id})  # payload
    return {"access_token": access_token, "token_type": "bearer"}
