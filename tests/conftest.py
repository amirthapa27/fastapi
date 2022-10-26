from fastapi.testclient import TestClient
from app.database import get_db, Base
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pytest
from app.oauth2 import create_access_token
from app import models

SQLALCHEMY_DATABSE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

# connnects sqlalchemy to pstgres database
engine = create_engine(SQLALCHEMY_DATABSE_URL)
# inorder to talk to the database
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


# use this to create a database session and close it after finishing.


# app.dependency_overrides[get_db] = override_get_db  # swap the dependencies


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):

    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db  # swap the dependencies
    # run our code before we run  our test
    yield TestClient(app)
    # run our code after we finish our test


@pytest.fixture
def test_user2(client):
    user_data = {"email": "amir27@gmail.com", "password": "unlock123"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    # print(response.json)
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_user(client):
    user_data = {"email": "amir@gmail.com", "password": "unlock123"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    # print(response.json)
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


# fixture that will create a few initial posts
@pytest.fixture
def tests_post(test_user, session, test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user2['id']
    }
    ]

    def create_post_model(post):  # for adding the posts into the table
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)  # returns a map
    posts = list(post_map)  # converts into list
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts
