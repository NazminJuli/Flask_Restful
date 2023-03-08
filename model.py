
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()

class Parents(db.Model):
    # parent model
    __tablename__ = 'parent'
    # unique user id
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    # Here for simplicity parent's name field has been made as UNIQUE
    firstname = db.Column(db.String(25), unique=True, nullable=False)
    lastname = db.Column(db.String(25), unique=True, nullable=False)
    street = db.Column(db.String(25), nullable=False)
    city = db.Column(db.String(25), nullable=False)
    state = db.Column(db.String(25), nullable=False)
    zip_code = db.Column(db.String(25), nullable=False)


class Child(db.Model):
    # Child model
    __tablename__ = 'child'

    id = db.Column(db.Integer, primary_key= True, autoincrement = True)

    child_firstname = db.Column(db.String(25), unique=False, nullable=False)
    child_lastname = db.Column(db.String(25), unique=False, nullable=False)

    # make a relationship with 'Child' model
    parent_id = db.Column(db.Integer, ForeignKey('parent.id', ondelete="cascade"), nullable=False)
    pcrel = db.relationship('Parents',  backref = (db.backref("child", cascade="all, delete, delete-orphan")) )




