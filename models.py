from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Model for User"""

    __tablename__ = "users"
    id = db.Column(db.Integer,
                            primary_key = True,
                            autoincrement = True)
    username = db.Column(db.String(20),
                            nullable = False,
                            unique = True)
    password = db.Column(db.Text,
                            nullable = False)
    email = db.Column(db.String(50),
                            nullable = False,
                            unique = True)
    first_name = db.Column(db.String(30),
                            nullable = False)
    last_name = db.Column(db.String(30),
                            nullable = False)
    
    def __repr__(self):
        user = f"<User ID: {self.id}; Name: {self.first_name} {self.last_name};"
        auth = f" Username: {self.username}; Email: {self.email}>"
        return f"{user} {auth}"