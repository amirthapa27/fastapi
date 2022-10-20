from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from app import oauth2
from sqlalchemy import func
from app.database import get_db
from .. import schemas, models, utils

router = APIRouter(
    prefix="/posts",  # we do not have to mention /post again and again
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # posts = db.query(models.Post).filter(models.Post.owner_id ==
    #  current_user.id).all()  # for getting only the suers posts
    # cursor.execute("""SELECT * FROM posts """)  # sql commands
    # posts = cursor.fetchall()  # to fetch all the data

    posts = db.query(models.Post, func.count(models.Vote.user_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(results)

    return posts


@ router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
# refrencing the pydantic model
def create_posts(post: schemas.PostCretae, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # # print(post)
    # # print(post.dict())  # converting pydantic model into dictionary
    # # post_dict = post.dict()
    # # post_dict['id'] = randrange(0, 10000000)
    # # my_posts.append(post_dict)
    # cursor.execute("""INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()  # will push the post into the databas

    # **post.dict will unpack the dictionary
    # print(current_user.id)
    new_post = models.Post(owner_id=current_user.id, ** post.dict())

    db.add(new_post)  # add it to the database
    db.commit()  # commit the changes
    db.refresh(new_post)  # same as RETURNING* iin sql
    return new_post


# to get a sinlge post through id
# define a decorator and get
@ router.get("/{id}", response_model=schemas.PostOut)
# the id will be extracted by fast api and only int field types will be accepted
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    # # to manupulate the response
    # # post = find_post(id)
    # filter is same as where is sql and
    post = db.query(models.Post, func.count(models.Vote.user_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    # print(post)

    return post


# delete post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(
    #     """DELETE FROM POSTS WHERE id = %s RETURNING * """, (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    # # index = find_index_post(id)
    # if index doesnt exist
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

    if post.owner_id != current_user.id:  # same user id can manupulate the post
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    post_query.delete(synchronize_session=False)
    db.commit()
    # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCretae, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    # index = find_index_post(id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    # post_dict = post.dict()  # convert it into normal python dict
    # post_dict['id'] = id  # add the id
    # my_posts[index] = post_dict
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
