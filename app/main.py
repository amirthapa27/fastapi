from fastapi import FastAPI
from app.config import settings
from . import models
from .database import engine
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware


print(settings.database_username)

# models.Base.metadata.create_all(bind=engine)  # create all of our tables
app = FastAPI()

# all of the domains that can talk to our api
origins = ["*"]
app.add_middleware(
    CORSMiddleware,  # function that runs before evry request
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)  # includes post file from router folder
app.include_router(user.router)  # includes user file from router folder
app.include_router(auth.router)  # includes auth file from router folder
app.include_router(vote.router)  # includes vote file from router folder


@app.get("/")
async def root():
    return {"message": "Hello world"}


# create a session once the rquest is done then close it


# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()  # creating query to get all
#     return {"message": posts}
