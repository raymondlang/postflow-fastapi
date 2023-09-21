from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel

from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from . import models, schemas, utils
from .database import engine, get_db

app = FastAPI()

class Post(BaseModel):
        title: str
        content: str
        published: bool = True

try:
    conn = psycopg2.connect(host= 'localhost', database='fastapi', user='postgres', password='123456', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection successful!")
except Exception as error:
    print("Connection failed")
    print("Error: ", error)

my_posts = [{"title": "title 1", "content": "content1", "id": 1}]

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor. execute("""INSERT INTO posts (title, content, published) VALUES (%, %5, %5) RETURNING *""",
                    (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn. commit()
    return new_post

@app.get ("/posts/{id}")
def get_post(id: int):
    cursor .execute("""SELECT * from posts WHERE id = %§ """, (str(id),))
    post = cursor.fetchone()
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_484_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

#     post_dict = post.dict()
#     post_dict['id'] = randrange(0, 1000000)
#     my_posts.append (post_dict)
#     return {"data": post_dict}

def find_post(id):
     for p in my_posts:
          if p['id'] == id:
            return p

def find_index_post(id):
     for i, p in enumerate(my_posts):
          if p['id'] == id:
               return i

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
     new_post = models.Post(**post.dict())
     db.add(new_post)
     db.commit()
     db.refresh(new_post)

@app.get("/posts/{id}")
def get_post (id: int, response: Response):
    print(id)
    return {"post_detail": f"Here is post {id}"}

@app.delete("/posts/{id}")
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id =%s returning *""", (str(id),))
    deleted_post=cursor.fetchone()
    conn.commit()

    if deleted_post == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with id {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
     hashed_password = utils.hash(user.password)
     user.password = hashed_password

     new_user = models.User(**user.dict())
     db.add(new_user)
     db.commit()
     db.refresh(new_user)

     return new_user
