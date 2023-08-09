from fastapi import FastAPI
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

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

@app.post("/posts")
def create_posts(post:Post):
     print(post)
     print(post.dict())
     return {"data":post}

@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append (post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post (id):
    print(id)
    return {"post_detail": f"Here is post {id}"}
