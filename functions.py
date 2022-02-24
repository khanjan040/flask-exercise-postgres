# #from mockdb.dummy_data import initial_db_state
# import json

# from flask import Flask
# import sqlalchemy

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Khanjan0611$@localhost:5433/cars_api"
# db = sqlalchemy(app)
# db_state = db


# def get(type):
#     return db_state[type]


# def getById(type, id):
#     return next((i for i in get(type) if i["id"] == id), None)


# def create(type, payload):
#     last_id = max([i["id"] for i in get(type)])
#     new_id = last_id + 1
#     payload["id"] = new_id
#     db_state[type].append(payload)
#     return payload


# def updateById(type, id, update_values):
#     item = getById(type, id)
#     if item is None:
#         return None
#     for k, v in update_values.items():
#         if k != "id":
#             item[k] = v
#     return item


# def deleteById(type, id):
#     db_state[type] = [i for i in get(type) if i["id"] != id]
