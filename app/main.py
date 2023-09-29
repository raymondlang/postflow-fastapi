from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth, vote

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# while True:

#     try:
#         conn = psycopg2.connect(host= 'localhost', database='fastapi', user='postgres', password='123456', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection successful!")
#     except Exception as error:
#         print("Connection failed")
#         print("Error: ", error)
#         time.sleep(2)

#     post_dict = post.dict()
#     post_dict['id'] = randrange(0, 1000000)
#     my_posts.append (post_dict)
#     return {"data": post_dict}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello World"}
