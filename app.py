from typing import Tuple
from flask import Flask, Response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import null
import functions as dbb

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Khanjan0611$@postgresdb:5432/users_db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class UsersModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    team = db.Column(db.String())
    age = db.Column(db.Integer())

    def __init__(self, name, team, age):
        self.name = name
        self.age = age
        self.team = team

    def __repr__(self):
        return f"<User {self.name}>"

# app = Flask(__name__)

def create_response(
    data = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.

    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if data is None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status

@app.route('/')
def hello():
    return {"hellollll": "world, yes its this"}

# @app.route("/")
# def hello_world():
#     return create_response({"content": "hello world!"})


@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)

@app.route('/users',  methods=['POST', 'GET'])
def users():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_user = UsersModel(name=data['name'], team=data['team'], age=data['age'])
            db.session.add(new_user)
            db.session.commit()
            return {"message": f"User {new_user.name} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}
    
    elif request.method == 'GET':
        users = UsersModel.query.all()
        results = [
            {
                "name": user.name,
                "age": user.age,
                "team": user.team
            } for user in users]
        
        return {"count": len(results), "users": results}

@app.route('/users/<id>', methods=['GET'])
def spid(id):
    if request.method == 'GET':
        users = UsersModel.query.all()
        results = []
        for user in users:
            if user.id == int(id):
                dict = {
                        "name": user.name,
                        "age": user.age,
                        "team": user.team
                        }
                results.append(dict)

        if results != None:
            return {"count": len(results), "users": results}
        else:
            return {"error": "Unexpected Error"}


# @app.route("/users/teams")
# def users_query():
#     var = request.args.get("team")
#     print(var)
#     data = db.get("users")
#     temp=[]
#     for user in data:
#         if user['team'] == var:
#             temp.append(user)
#     return create_response(temp)

@app.route("/createuser", methods = ['POST'])
def createuser():
    temp = request.json
    data = db.create("users",temp)
    return create_response(data)

@app.route("/users/<id>", methods = ['PUT'])
def update(id):
    temp = request.json
    data = db.updateById("users", int(id),temp)
    if data is None:
        return ({"status": 404, "message":"User not found"})
    return create_response(data)

@app.route("/users/<id>", methods = ['DELETE'])
def delete(id):
    db.deleteById("users", int(id)) is not None
    if db.get("users") is not None:
        return {"status": 200, "message":"User Deleted Successfully"}
    else:
        return {"status": 404, "message":"Unsuccessfully"}

# TODO: Implement the rest of the API here!

    """
    ~~~~~~~~~~~~ END API ~~~~~~~~~~~~
    """
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")