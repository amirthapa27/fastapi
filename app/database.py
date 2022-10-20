from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2  # for connecting the database
import time
from psycopg2.extras import RealDictCursor

from app.config import settings


# SQLALCHEMY_DATABSE_URL = 'postgressql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABSE_URL = f'postgresql://{settings.database_username}:{settings.databse_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# connnects sqlalchemy to pstgres database
engine = create_engine(SQLALCHEMY_DATABSE_URL)
# inorder to talk to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# use this to create a database session and close it after finishing.


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:  # will keep running untill database is connected
#     try:  # using try inorder to know if the connection has failed
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
#                                 password='mypass', port=5434, cursor_factory=RealDictCursor)  # connecting to the database
#         cursor = conn.cursor()  # opens a cursor to perform database operation
#         print("Database connection was successfull")
#         break
#     except Exception as error:
#         print("Connection to the database failed")
#         print("Error", error)
#         time.sleep(3)
