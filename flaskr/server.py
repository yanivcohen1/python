from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from json import dumps
from flask import jsonify
import json

app = Flask(__name__)
api = Api(app)
""" def test() -> str:
    a = 1
    return a
a : int = test() """
CORS(app)
employees = {"employees": [{"id": 1, "name": "Balram"}, {"id": 2, "name": "Tom"}]}


@app.route("/")
def hello():
    return jsonify({"text": "Hello World!"})


class Employees(Resource):
    def get(self):
        return employees


class Employees_Name(Resource):
    def get(self, employee_id):
        print("Employee id:" + employee_id)
        # parse x:
        # employees = json.loads(employees_json) # for convert json string to dictionary
        employee = employees["employees"][
            int(employee_id)
        ]  # {'data': {'id':1, 'name':'Balram'}}
        result = {"data": employee}
        return jsonify(result)

    def post(self):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass


api.add_resource(Employees, "/employees")  # Route_1
api.add_resource(Employees_Name, "/employees/<employee_id>")  # Route_3

print("server.py")
if __name__ == "__main__":
    app.run(debug=True, port=5002)  # debug will reload the saved changes
