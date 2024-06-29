import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String,Enum
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship 
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    firstname = Column(String(250), nullable=False)
    lastname = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)

    posts = relationship('Post', back_populates='user')
    comments = relationship('Comment', back_populates='user')
    media = relationship('Media', back_populates='user')
    followers = relationship('Follower', foreign_keys='Follower.user_from_id', back_populates='user_from')
    following = relationship('Follower', foreign_keys='Follower.user_to_id', back_populates='user_to')

class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    comment_id = Column(String, ForeignKey('comment.id'))
    user = relationship(User)
    comments = relationship('Comment', back_populates='post')
    media = relationship('Media', back_populates='post')

class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(250), nullable=False)
    author_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    user = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')
    

class Media(Base):
    __tablename__ = "media"
    id = Column(Integer, ForeignKey('user.id'))
    type = Column(Enum("reel","carrousel","history"), nullable=False)
    url = Column(String(250), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship('Post', back_populates='media')
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='media')
    
class Follower(Base):
    __tablename__ = "follower"
    user_from_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user_to_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user_from = relationship('User', foreign_keys=[user_from_id], back_populates='followers')
    user_to = relationship('User', foreign_keys=[user_to_id], back_populates='following')




    # __tablename__ = 'person'
    # # Here we define columns for the table person
    # # Notice that each column is also a normal Python instance attribute.
    # id = Column(Integer, primary_key=True)
    # name = Column(String(250), nullable=False)

# class Address(Base):
    # __tablename__ = 'address'
    # # Here we define columns for the table address.
    # # Notice that each column is also a normal Python instance attribute.
    # id = Column(Integer, primary_key=True)
    # street_name = Column(String(250))
    # street_number = Column(String(250))
    # post_code = Column(String(250), nullable=False)
    # person_id = Column(Integer, ForeignKey('person.id'))
    # person = relationship(Person)

    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
