from flask import Flask
from flask.views import MethodView
from flask_smorest import Api, Blueprint
from marshmallow import Schema, fields
from pymongo import MongoClient

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/marshmallow"
client = MongoClient(app.config["MONGO_URI"])
db = client.get_database()

# 1. Configure Swagger/OpenAPI settings
app.config["API_TITLE"] = "My API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

# 2. Define your Marshmallow Schema
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)

blp = Blueprint("users", "users", description="Operations on users")

# 3. Use decorators to link Schema to Swagger
@blp.route("/user")
class User(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        """Get all users"""
        users: UserSchema = list(db.users.find({}, {"_id": 0}))
        return users

    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, new_data: UserSchema):
        """Create a new user"""
        last_user = db.users.find_one(sort=[("id", -1)])
        new_id = last_user["id"] + 1 if last_user and "id" in last_user else 1
        new_data["id"] = new_id
        db.users.insert_one(new_data)
        new_data.pop("_id", None)
        return new_data

api.register_blueprint(blp)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=5000) # http://127.0.0.1:5000/swagger-ui
