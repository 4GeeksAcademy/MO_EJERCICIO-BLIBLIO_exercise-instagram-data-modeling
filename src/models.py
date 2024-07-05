# import os
# import sys
# from sqlalchemy import Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship, declarative_base
# from sqlalchemy import create_engine
# from eralchemy2 import render_er

# # importacion flask
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
# db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

#     def __repr__(self):
#         return f'<User {self.username}>'

# if __name__ == '__main__':
#     app.run(debug=True)

# # final exportacion

# Base = declarative_base()

# # class Person(Base):
# #     __tablename__ = 'person'
# #     # Here we define columns for the table person
# #     # Notice that each column is also a normal Python instance attribute.
# #     id = Column(Integer, primary_key=True)
# #     name = Column(String(250), nullable=False)

# class Follower(Base):
#     __tablename__ = 'follower'
#     # Here we define columns for the table address.
#     # Notice that each column is also a normal Python instance attribute.
#     id = Column(Integer, primary_key=True)
#     user_to_id = Column(String(250))
    

# class User(Base):
#     __tablename__ = 'usernamer'
#     # Here we define columns for the table address.
#     # Notice that each column is also a normal Python instance attribute.
#     id = Column(Integer, primary_key=True)
#     username = Column(String(250))
#     firstname = Column(String(250))
#     lastname = Column(String(250), nullable=False)
#     email = Column(Integer, ForeignKey('person.id'))
  

# class Media(Base):
#     __tablename__ = 'media'
#     # Here we define columns for the table address.
#     # Notice that each column is also a normal Python instance attribute.
#     id = Column(Integer, ForeignKey('medio.id')
#     Type = Column(String(250))
#     url = Column(String(250))
#     post_id = Column(String(250), nullable=False)

# class Post(Base):
#     __tablename__ = 'post'
#     # Here we define columns for the table address.
#     # Notice that each column is also a normal Python instance attribute.
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('person.id'))
    
# class Comment(Base):
#     __tablename__ = 'comment'
#     # Here we define columns for the table address.
#     # Notice that each column is also a normal Python instance attribute.
#     id = Column(Integer, primary_key=True)
#     comment_text = Column(String(250))
#     author_id = Column(String(250))
#     person_id = Column(Integer, ForeignKey('person.id'))
    

    
# # class follower(Base):
# #     __tablename__ = 'Follower'
# #     # Here we define columns for the table address.
# #     # Notice that each column is also a normal Python instance attribute.
# #     id = Column(Integer, primary_key=True)
# #     street_name = Column(String(250))
# #     street_number = Column(String(250))
# #     post_code = Column(String(250), nullable=False)
# #     person_id = Column(Integer, ForeignKey('person.id'))
# #     person = relationship(Person)




#     def to_dict(self):
#         return {}

# ## Draw from SQLAlchemy base
# try:
#     result = render_er(Base, 'diagram.png')
#     print("Success! Check the diagram.png file")
# except Exception as e:
#     print("There was a problem genering the diagram")
#     raise e

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, long
from sqlalchemy.orm import relationship, declarative_base
from eralchemy2 import render_er  # type: ignore

# importación Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80), unique=True, nullable=False)
    firstname = Column(String(250))
    lastname = Column(String(250), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    posts = relationship('Post', back_populates='user')
    comments = relationship('Comment', back_populates='author')
    followers = relationship('Follower', foreign_keys='Follower.user_to_id', back_populates='user_to', lazy=True)
    following = relationship('Follower', foreign_keys='Follower.user_from_id', back_populates='user_from', lazy=True)

class Follower(Base):
    __tablename__ = 'follower'
    id = Column(Integer, primary_key=True)
    user_to_id = Column(Integer, ForeignKey('user.id'))
    user_from_id = Column(Integer, ForeignKey('user.id'))
    user_to = relationship('User', foreign_keys=[user_to_id], back_populates='followers', lazy=True)
    user_from = relationship('User', foreign_keys=[user_from_id], back_populates='following', lazy=True)

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    type = Column(String(250))
    url = Column(String(250))
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    post = relationship('Post', back_populates='media', lazy=True)

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='posts')
    media = relationship('Media', back_populates='post')
    comments = relationship('Comment', back_populates='post', lazy=True)

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(250))
    author_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    author = relationship('User', back_populates='comments', lazy=True)
    post = relationship('Post', back_populates='comments', lazy=True)

# Crear la base de datos
engine = create_engine('sqlite:///example.db')
Base.metadata.create_all(engine)

# Generar el diagrama ER
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e

if __name__ == '__main__':
    app.run(debug=True)
