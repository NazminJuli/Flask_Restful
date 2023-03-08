# FlaskRestful_one2many

## Features
- Database model has been designed according to one to many parent-child relationship, where every children belongs to one parent.
- Here is the code blocks of the model
```sh

    # make a relationship with 'Child' model
    parent_id = db.Column(db.Integer, ForeignKey('parent.id', ondelete="cascade"), nullable=False)
    pcrel = db.relationship('Parents',  backref = (db.backref("child", cascade="all, delete, delete-orphan")) )
    
    In a one to many model, when parent node is deleted, associated children entry should also be removed, hence
    cascade delete has been added here
```
- I have used Flask-RESTful **fields** to render the **nested resources** 
- The decorator **marshal_with** has been used to format the response
- ***localhost/parent***  has POST,GET,PUT,DELETE operation where ***Update*** works on parent's address
- ***localhost/child*** has POST,GET,DELETE operation 
- Each HTTP request has ***JSON*** formated status and message as response.
- **Postman** has been used to send request

## Tools Used
- python (3.7.6) Windows Version
- Flask (2.2.2)
- Werkzeug (2.2.2)
- Flask SQLAlchemy (2.0.3)
- Flask RESTful
- Postman

## Installation
We need to install Flask-RESTful, the light-weight Flask extention to build REST API quickly.
```sh
pip install python

pip install Flask-SQLAlchemy
pip install Flask-RESTful
```


