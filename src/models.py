import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String,Enum, Table
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship 
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

Followers = Table(
    'followers',
    Base.metadata,
    Column('follower_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('following_id', Integer, ForeignKey('user.id'), primary_key=True),
)

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    firstname = Column(String(250), nullable=False)
    lastname = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    posts = relationship('Post', backref='user')
    comments = relationship('Comment', backref='user')
    media = relationship('Media', backref='user')
    followed = relationship(
        'User',
        secondary = Followers,
        primaryjoin=(Followers.c.following_id == id),
        secondaryjoin=(Followers.c.follower_id == id),
        backref="following",
        lazy=True
    
)

class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    comment_id = Column(String, ForeignKey('comment.id'))
    user = relationship(User)
    comments = relationship('Comment', backref='post')
    media = relationship('Media', backref='post')

class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(250), nullable=False)
    author_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    user = relationship('User', backref='comments')
    post = relationship('Post', backref='comments')
    

class Media(Base):
    __tablename__ = "media"
    id = Column(Integer, primary_key=True)
    type = Column(Enum("reel","carrousel","history"), nullable=False)
    url = Column(String(250), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship('Post', backref='media')
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', backref='media')
    
class Follower(Base):
    __tablename__ = "follower"
    follower_id = Column(Integer, primary_key=True)
    following_id = Column(Integer, primary_key=True)



    # user_to_id = Column(Integer, primary_key=True)
    




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
