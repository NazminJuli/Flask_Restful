from model import db, Parents, Child
from flask_restful import Resource, Api, fields, marshal_with
from flask import Flask, request, jsonify, json

app = Flask(__name__)
SECRET_KEY = 'secret key'

# # Configure Flask by providing the SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/MTT/PycharmProjects/One2Many/database.db'
app.config['SECRET_KEY'] = SECRET_KEY

api = Api(app)
db.init_app(app)

with app.app_context():
    db.create_all()

### Declare fields to add in Resource
child_fields = {
    'id': fields.Integer,
    'child_firstname': fields.String,
    'child_lastname': fields.String
}

parent_fields = {
    'id': fields.Integer,
    'firstname': fields.String,
    'lastname': fields.String,
    'street': fields.String,
    'city': fields.String,
    'state': fields.String,
    'zip_code': fields.String,
    'child': fields.Nested(child_fields)
    }

child_fields_withid = {
    'id': fields.Integer,
    'child_firstname': fields.String,
    'child_lastname': fields.String,
    'parent_id': fields.Integer

}


class ParentList(Resource):
    response = {"status": 400, "message": "Parent not created"}

    @marshal_with(parent_fields)
    def get(self, pid=None):
        if pid is not None:
            get_parent = Parents.query.filter_by(id=pid).first()
            return get_parent

        else:
            self.response["message"] = "Parent ID is required"
            return self.response, 400

    def post(self):
        parent_data = request.json
        firstname = parent_data["firstname"]
        lastname = parent_data["lastname"]
        street = parent_data["street"]
        city = parent_data["city"]
        state = parent_data["state"]
        zip_code = parent_data["zip_code"]

        if db.session.query(Parents).filter_by(firstname=firstname).scalar() or db.session.query(Parents).filter_by(lastname=lastname).scalar() is not None:
            self.response["message"] = "User name already existed"

        else:
            parent_entry = Parents(firstname = firstname, lastname = lastname, street = street, city = city, state = state, zip_code = zip_code)
            db.session.add(parent_entry)
            db.session.commit()

#            self.response["status"] = 201
            self.response["message"] = "New Parent created successfully"

        return self.response, 201

    def delete(self, pid=None): # Delete Parent by id along its related child table

        if pid is not None:
            try:
                get_parent = Parents.query.filter_by(id=pid).first()
                db.session.delete(get_parent)
                db.session.commit()
                self.response["message"] = "Record deleted successfully"
                return self.response, 201
            except:
                self.response["message"] = "Record not found"
                return self.response, 404
        else:
            self.response["message"] = "ID is required"
            return self.response, 400

    def put(self, pid=None): # Update parent's address street, city, state, zip code
        if pid is not None:
            user = Parents.query.filter_by(id=pid).first()
            if user is not None:
                data = request.json
                user.street = data['street']
                user.city = data['city']
                user.state = data['state']
                user.zip_code = data['zip_code']
                db.session.commit()
                self.response["message"] = "Record successfully updated"
                return self.response, 201
            else:
                self.response["message"] = "Record not found"
                return self.response, 404

        else:
            self.response["message"] = "Id is required"
            return self.response, 400


class ChildList(Resource):
    response = {"status": 400, "message": "Child not created"}

    @marshal_with(child_fields_withid)
    def get(self, pid=None): # get child list by its parent ID
      if pid is not None:
        get_child = Child.query.filter_by(parent_id=pid)
        flag = db.session.query(get_child.exists()).scalar()
        if flag:
            all_childs = []
            for child in get_child:
                child_details = {
                    "id": child.id,
                    "child_firstname": child.child_firstname,
                    "child_lastname": child.child_lastname,
                    "parent_id": child.parent_id,
                }
                all_childs.append(child_details)

            self.response["message"] = all_childs
            return self.response["message"], 200

        else:
            data = Child.query.all()
            self.response["message"] = "corresponding parent id not available"
            return self.response["message"], 404

      else:
          self.response["message"] = "corresponding ID is required"
          return self.response["message"], 400

    def post(self):
        data = request.json
        firstname = data["child_firstname"]
        lastname = data["child_lastname"]
        parent_id = data["parent_id"]

        if firstname == ' ' or lastname == ' 'or parent_id == ' ':
            self.response["message"] = "Enter all fields"
            return self.response["message"]

        if db.session.query(Parents).filter_by(firstname = firstname).scalar() and db.session.query(Parents).filter_by(lastname=lastname).scalar() is not None:
            self.response["message"] = "Duplicate Entry"
            return self.response["message"]

        child_entry = Child(child_firstname=firstname, child_lastname=lastname, parent_id=parent_id)
        db.session.add(child_entry)
        db.session.commit()

        self.response["status"] = 201
        self.response["message"] = "New Child created successfully"

        return self.response, 201

    # def delete(self, pid=None):
    #
    #     if pid is not None:
    #         try:
    #             get_child = Child.query.filter_by(parent_id=pid).first()
    #             db.session.delete(get_child)
    #             db.session.commit()
    #             self.response["message"] = "Record deleted successfully"
    #             return self.response, 201
    #
    #         except:
    #             self.response["message"] = "Record not found"
    #             return self.response, 404
    #     else:
    #         self.response["message"] = "ID is required"
    #         return self.response, 400

    def put(self, pid=None): # update child name
        if pid is not None:
            user = Child.query.filter_by(parent_id=pid).first()
            if user is not None:
                data = request.json
                user.child_firstname = data['child_firstname']
                user.child_lastname = data['child_lastname']
                #user.parent_id = data['parent_id']

                db.session.commit()

                return {"message": " Child Record successfully updated"}, 201
            else:
                return {"message": "Record not found"}, 404
        else:
            return {"message": "Id is required"}, 400

#add resource
api.add_resource(ParentList, "/parent", "/parent/<int:pid>")
api.add_resource(ChildList, "/child", "/child/<int:pid>")


if __name__ == '__main__':
    app.run(debug=True)
