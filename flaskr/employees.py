from flask import Blueprint
from flask import session
from flask import request
from flask import jsonify

bp = Blueprint("employees", __name__, url_prefix="/employees")
# errors = Blueprint('errors', __name__)
employeess = {"employees": [{"id": 1, "name": "Balram"}, {"id": 2, "name": "Tom"}]}
# for seralization use cast-class-json-class.py
# see for mysql + rest - rest_crud_mysql folder
import json

dictionary1 = {"employees": [{"id": 1, "name": "Balram"}, {"id": 2, "name": "Tom"}]}
# convert dictionary into JSON:
json1 = json.dumps(dictionary1)
# the result is a JSON string:
# print(y)
# conver JSON to dictionary
employeess = json.loads(json1)


@bp.route("/")  # , methods=("GET", "POST", "PUT", "DELETE")
def employees():
    """Clear the current session, including the stored user id."""
    # for GET
    # user_id = session.get("user_id")

    # for POST
    # username = request.form["username"]

    # for PUT
    # _json = request.json
    # _id = _json['id']

    # for DELETE
    # @app.route('/delete/<int:id>', methods=['DELETE'])
    # def delete_user(id):

    # for HEADER
    # request.headers.get('your-header-name')

    # for Costume HEADER Response
    # resp = flask.make_response()
    # resp.headers["custom-header"] = "custom"
    # resp.status = 200 # not mast
    # resp.mimetype='application/json # not mast
    # resp.response=json.dumps(data) # not mast
    # return resp

    # for Error return
    # return flask.make_response(jsonify(message='Failed to create chain', error=e.message), http_code)
    return employeess


@bp.route("/<employee_id>")
def get(employee_id):
    print("Employee id:" + employee_id)
    result = employeess["employees"][int(employee_id) - 1][
        "name"
    ]  # {'data': {'id':employee_id, 'name':'Balram1'}}
    # send as mimetype='application/json'
    return jsonify(result)  # str(result)


# for coustume error
# @errors.app_errorhandler(Exception)
# def handle_error(error):
#     message = [str(x) for x in error.args]
#     status_code = error.status_code
#     success = False
#     response = {
#         'success': success,
#         'error': {
#             'type': error.__class__.__name__,
#             'message': message
#         }
#     }
#     return jsonify(response), status_code
