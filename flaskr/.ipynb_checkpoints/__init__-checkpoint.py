import os
from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from json import dumps
# from flask_jsonpify import jsonify

# request.headers.get('your-header-name') // read from header parameters
# session.get("user_id") // read from session parameters
# request.args.get('username') // read from url parameters
# if request.method == "POST": // not mast
#        username = request.form.get("user_id") // read post parameters

# init
def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    print('_init_.py')
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # register the database commands
    from flaskr import db

    db.init_app(app)

    # apply the blueprints to the app
    from flaskr import auth, blog

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    # add by yaniv for angular
    api = Api(app)
    CORS(app)
    # if Employees class is from file then
    # from folderName import fileName
    # from .folder.folder import fileName //nested dir
    # from . import fileName //current dir
    # from ...folder.folder import fileName // three backwords dirs
    # fileName.className
    #api.add_resource(Employees, '/employees') # Route_1
    #api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_3
    #for angular
    from flaskr import employees
    app.register_blueprint(employees.bp)
    #app.register_blueprint(employees.errors)
    #end config
    return app

# for seralization use cast-class-json-class.py
# see for mysql + rest - rest_crud_mysql folder
# @bp.route("/") #, methods=("GET", "POST", "PUT", "DELETE")
# def employees():
#   """Clear the current session, including the stored user id."""
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
    #return flask.make_response(jsonify(message='Failed to create chain', error=e.message), http_code)

# add by yaniv for angular
# class Employees(Resource):
#     def get(self):
#         return {'employees': [{'id':1, 'name':'Balram'},{'id':2, 'name':'Tom'}]}

# class Employees_Name(Resource):
#     def get(self, employee_id):
#         print('Employee id:' + employee_id)
#         result = {'data': {'id':1, 'name':'Balram'}}
#         return jsonify(result)
