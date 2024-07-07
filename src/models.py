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
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    username = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)

class Followers(Base):
    __tablename__ = 'followers'
    id = Column(Integer, primary_key=True)
    accepted = Column(Boolean)

    # Relación: Muchos seguidores pertenecen a un usuario
    follower_id = Column(Integer, ForeignKey('users.id'))
    follower = relationship('Users', foreign_keys=[follower_id])
    # Relación: Muchos seguidores están asociados a un usuario
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('Users', foreign_keys=[user_id])
    

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    photo = Column(String(50))
    description = Column(String(250))

    # Relación: Muchos posts pertenecen a un usuario
    user_id = Column(Integer, ForeignKey('users.id'))
    users = relationship(Users)
    
    # Relación: Un post puede tener muchos comentarios
    post_id_comments = Column(Integer, ForeignKey('posts.id'))
    comments = relationship('Comments')  
    

class Likes(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True)

    # Relación: Muchos likes pertenecen a un usuario
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(Users)  

    # Relación: Muchos likes están asociados a un post
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship(Post)   
    

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    url = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)

    # Relación: Muchos medios pertenecen a un usuario
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(Users)  
    

class Comments(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    text = Column(String(250))

    # Relación: Muchos comentarios pertenecen a un usuario
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(Users)  

    # Relación: Muchos comentarios están asociados a un post
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship(Post)   


## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e