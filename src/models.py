import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Table, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

Followers = Table(
    'followers',
    Base.metadata,
    Column('follower_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('following_id', Integer, ForeignKey('user.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'user'
    ID = Column(Integer, primary_key=True)
    user_name = Column(String(250), nullable=False)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    post = relationship('Post', backref='user', lazy=True)
    comment = relationship('Comment', backref='user', lazy=True)
    followed = relationship(
        'User',
        secondary = Followers,
        primaryjoin = (Followers.c.following_id == id),
        secondaryjoin = (Followers.c.follower_id == id),
        backref = "following",
        lazy = True
    )
    
class Media(Base):
    __tablename__='media'
    ID = Column(Integer, primary_key=True)
    type = Column(Enum('photo', 'video', 'reel'), nullable=False)
    url = Column(String(250), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'))

class Post(Base):
    __tablename__='post'
    ID = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('user.id'))
    comment = relationship('Comment', backref='post', lazy=True)
    user_id = Column(Integer, ForeignKey('user.id'))

class Comment(Base):
    __tablename__='Comment'
    ID = Column(Integer, primary_key=True)
    comment_text = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id')),
    post_id = Column(Integer, ForeignKey('post.id'))


# class Person(Base):
#     __tablename__ = 'person'
#     # Here we define columns for the table person
#     # Notice that each column is also a normal Python instance attribute.
#     id = Column(Integer, primary_key=True)
#     name = Column(String(250), nullable=False)

# class Address(Base):
#     __tablename__ = 'address'
#     # Here we define columns for the table address.
#     # Notice that each column is also a normal Python instance attribute.
#     id = Column(Integer, primary_key=True)
#     street_name = Column(String(250))
#     street_number = Column(String(250))
#     post_code = Column(String(250), nullable=False)
#     person_id = Column(Integer, ForeignKey('person.id'))
#     person = relationship(Person)

#     def to_dict(self):
#         return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
