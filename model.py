
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
#
#
# app = Flask(__name__)
#
# SECRET_KEY = 'secret key'
#
# # Configure Flask by providing the SQLALCHEMY_DATABASE_URI
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/MTT/PycharmProjects/One2Many/database.db'
#
# app.config['SECRET_KEY'] = SECRET_KEY
#
#
# # Model declaration
# # db = SQLAlchemy(app)
# # api = Api(app)
# api = Api()
# db = SQLAlchemy()
#
# api.init_app(app)
# db.init_app(app)
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

    # make a relationship with 'Child' model
    #parent_child_relation = db.relationship("Child", backref=db.backref("parent"), cascade="all, delete-orphan")

    #
    # def __init__(self, firstname, lastname, street, city, state, zip_code):
    #     self.firstname = firstname
    #     self.lastname = lastname
    #     self.street = street
    #     self.city = city
    #     self.state = state
    #     self.zip_code = zip_code


class Child(db.Model):
    # Child model
    __tablename__ = 'child'

    id = db.Column(db.Integer, primary_key= True, autoincrement = True)

    child_firstname = db.Column(db.String(25), unique=False, nullable=False)
    child_lastname = db.Column(db.String(25), unique=False, nullable=False)

    # make a relationship with 'Child' model
    parent_id = db.Column(db.Integer, ForeignKey('parent.id', ondelete="cascade"), nullable=False)
    pcrel = db.relationship('Parents',  backref = (db.backref("child", cascade="all, delete, delete-orphan")) )

    # def __init__(self, child_firstname, child_lastname, parent_id):
    #     self.child_firstname = child_firstname
    #     self.child_lastname = child_lastname
    #     self.parent_id = parent_id


