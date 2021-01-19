from fastapi import Depends, FastAPI, HTTPException, Request, File, UploadFile, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from typing import List, Dict
import os


from . import schemas
from .models import User, Post, Base
from .authentication import Auth
from .database import engine
from .utils import *

# Unfotunately this is a open issue in FastApi in github
middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'])
]

app = FastAPI(middleware=middleware)


Base.metadata.create_all(bind=engine)


@app.get("/")
async def main():
    return {"message": "OK!"}


@app.post("/users/", response_model=Dict[str, str])
def create_user(user: schemas.UserCreate):
    db_user = User.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(user)
    user.save()
    token = Auth.generate_token(user.id)
    return token


@app.post("/users/", response_model=Dict[str, str])
def login_user(user: schemas.UserLogin):
    user = User.get_user_by_email(email=user.email)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid Credentials")
    if not user.check_hash(user.password):
        raise HTTPException(status_code=400, detail="Invalid Credentials")
    token = Auth.generate_token(user.id)
    return token


@app.get("/users/", response_model=List[schemas.User])
def read_users(response: Response, skip: int = 0, limit: int = 100):
    users = User.get_users(skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int):
    user = User.get_user(user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/users/me", response_model=schemas.User)
@Auth.auth_required
def me_user(request: Request):
  user = User.get_user(request.state.user)
  return user


@app.get("/users/me", response_model=Dict[str, str])
@Auth.auth_required
def delete_user(request: Request):
  user = User.get_user(request.state.user)
  user.delete()
  return {'message': 'Deleted'}


@app.post("/posts/", response_model=schemas.Post)
@Auth.auth_required
def create_post_for_user(request: Request, post: schemas.PostCreate, image: UploadFile = File(...)):
    
    directory = dir_check_create()
    print(len(image.file))
    file_name = random_string(5) + image.filename
    with open(os.path.join(directory, '../media', file_name), 'wb') as local_file:
        local_file.write(image.file.read())
        local_file.close()
    post = Post(**post.dict(), photo=file_name, owner_id=request.state.user)
    post.save()
    return post


@app.get("/posts/", response_model=List[schemas.Post])
def read_posts(skip: int = 0, limit: int = 100):
    posts = Post.get_posts(skip=skip, limit=limit)
    return posts


@app.get("/posts/{post_id}", response_model=schemas.Post)
def read_user(post_id: int):
    post = Post.get_post(post_id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post



@app.delete("/posts/{post_id}", response_model=Dict[str, str])
@Auth.auth_required
def delete_post(request: Request, post_id):
  post = Post.get_post(post_id=post_id)
  if not post:
    raise HTTPException(status_code=404, detail="Post not found")
  if post.owner_id != request.state.user:
    raise HTTPException(status_code=400, detail="Permission denied")
  post.delete()
  return {'message': 'Deleted'}


@app.get("/download/{file_name}")
def download_file(file_name):
    directory = dir_check_create()
    return FileResponse(os.path.join(directory, '../media', file_name), media_type='application/octet-stream', filename=file_name)
