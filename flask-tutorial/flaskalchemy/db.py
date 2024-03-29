from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
# app.config['SECRET_KEY'] = 'dev'

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(50), nullable=False,unique=True)
    password = db.Column(db.String(50), nullable=False)
    address = db.relationship('Post', backref='user', lazy=True)

    def __init__(self,username, password):
        self.username = username
        self.password = generate_password_hash(password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    a_id = db.Column(db.Integer, db.ForeignKey('user.id') , nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    category=db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(500), nullable=False)

    def __init__(self, category,title, body, a_id):
        self.category=category
        self.title = title
        self.body = body
        self.a_id = a_id
