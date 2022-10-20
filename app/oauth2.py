# creating token
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from app import schemas, database, models
from sqlalchemy.orm import Session

from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')  # login endpoint

# secret key
# algorithm
# expiration time

# openssl rand -hex 32
# random long text
SECRET_KEY = settings.secret_key
ALGORITHM = settings. algorithm  # algorithm to be used
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes  # token expire time

# encoding


def create_access_token(data: dict):
    to_encode = data.copy()  # copying the data into to_encode
    # will add 30mins to current time
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # will encode and provide us jwt token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

# decoding


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=ALGORITHM)  # DECODING
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception  # going to raise whatever exception we provide
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data


# verify if the token is correct by calling the verify_access_token and extract the id
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
