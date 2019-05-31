from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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
    category = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(500), nullable=False)

    def __init__(self, title, body, a_id,category):
        self.category=category
        self.title = title
        self.body = body
        self.a_id = a_id
