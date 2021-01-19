from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

from .authentication import get_password_hash, verify_password
from .database import SessionLocal


Base = declarative_base()
db = SessionLocal()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    posts = relationship("Post", back_populates="owner")

    def __init__(self, user):
        self.name = user.name
        self.phone = user.phone
        self.email = user.email
        self.hashed_password = self.__generate_hash(user.password)

    def save(self):
        db.add(self)
        db.commit()

    def delete(self):
        db.delete(self)
        db.commit()
    
    @staticmethod
    def get_user_by_email(email: str):
        return db.query(User).filter_by(email=email).first()

    @staticmethod
    def get_users(skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def get_user(user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    def __generate_hash(self, password):
        return get_password_hash(password)
  
    def check_hash(self, password):
        return verify_password(password, self.hashed_password)


class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), index=True)
    contents = Column(Text)
    photo = Column(String(256))
    owner_id = Column(Integer, ForeignKey("users.id"))          
    owner = relationship("User", back_populates="posts")

    def save(self):
        db.add(self)
        db.commit()

    def delete(self):
        db.delete(self)
        db.commit()

    @staticmethod
    def get_posts(skip: int = 0, limit: int = 100):
        return db.query(Post).offset(skip).limit(limit).all()

    @staticmethod
    def get_post(post_id: int):
        return db.query(Post).filter(Post.id == post_id).first()
