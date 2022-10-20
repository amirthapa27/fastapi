from passlib.context import CryptContext

# defines the hashing algorithm to be used
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)

# verifying password


def verify(plain_password, hashed_password):
    # convert the plain password into hashed and verify if they are same
    return pwd_context.verify(plain_password, hashed_password)
