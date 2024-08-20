
#from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
#from eralchemy2 import render_er

#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)

#class User(db.Model):
    #__tablename__ = 'user'
#  #  id = db.Column(db.Integer, primary_key=True)
    #username = db.Column(db.String(250), nullable=False)
   # firstname = db.Column(db.String(250), nullable=False)
    #lastname = db.Column(db.String(250), nullable=False)
    #email = db.Column(db.String(250), nullable=False)

#class Post(db.Model):
   # __tablename__ = 'post'
    #id = db.Column(db.Integer, primary_key=True)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #user = db.relationship('User')

#class Comment(db.Model):
    #__tablename__ = 'comment'
    #id = db.Column(db.Integer, primary_key=True)
    #author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #author = db.relationship('User')
    #post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    #post = db.relationship('Post')

#class Media(db.Model):
   # __tablename__ = 'media'
    #id = db.Column(db.Integer, primary_key=True)
   # type = db.Column(db.String(250), nullable=False)
  #  url = db.Column(db.String(250), nullable=False)
    #post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    #post = db.relationship('Post')

#class Follower(db.Model):
    #__tablename__ = 'follower'
    #id = db.Column(db.Integer, primary_key=True)
    #user_from_id = db.Column(db.Integer, db.ForeignKey('user.id'))
   # user_from = db.relationship('User', foreign_keys=[user_from_id])
    #user_to_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #user_to = db.relationship('User', foreign_keys=[user_to_id])

#def to_dict(self):
    #return {}

## Draw from SQLAlchemy base
#try:
    #result = render_er(db.Model, 'diagram.png')
    #print("Success! Check the diagram.png file")
#except Exception as e:
    #print("There was a problem generating the diagram")
    #raise e

#if __name__ == '__main__':
    #with app.app_context():
       # db.create_all()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from eralchemy2 import render_er

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False)
    firstname = db.Column(db.String(250), nullable=False)
    lastname = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)

    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)

    # following = db.relationship('Follower', foreign_keys='Follower.user_from_id', backref='follower', lazy=True)
    # followers = db.relationship('Follower', foreign_keys='Follower.user_to_id', backref='followed', lazy=True)

# Relaciones muchos-a-muchos
    following = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.user_from_id == id),
        secondaryjoin=(followers.c.user_to_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
    )


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)
    media = db.relationship('Media', backref='post', lazy=True)

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

class Media(db.Model):
    __tablename__ = 'media'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(250), nullable=False)
    url = db.Column(db.String(250), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

class Follower(db.Model):
    __tablename__ = 'follower'
    id = db.Column(db.Integer, primary_key=True)
    user_from_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_to_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Definir las relaciones con los backref y lazy
    follower = db.relationship('User', foreign_keys=[user_from_id], backref=db.backref('following', lazy=True))
    followed = db.relationship('User', foreign_keys=[user_to_id], backref=db.backref('followers', lazy=True))

# Método to_dict para serialización
def to_dict(self):
    return {
        'id': self.id,
        'username': self.username,
        'firstname': self.firstname,
        'lastname': self.lastname,
        'email': self.email
    }

# Asociar el método to_dict a la clase User
User.to_dict = to_dict

## Dibujar el diagrama desde la base de SQLAlchemy
try:
    with app.app_context():
        result = render_er(db.Model, 'diagram.png')
        print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
