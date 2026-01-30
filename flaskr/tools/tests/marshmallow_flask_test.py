from flask import Flask
from flask_smorest import Api, Blueprint
from marshmallow import Schema, fields

app = Flask(__name__)

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
    @blp.response(200, UserSchema)
    def get(self):
        """Get a dummy user"""
        return {"id": 1, "name": "Jane Doe", "email": "jane@example.com"}

    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, new_data):
        """Create a new user"""
        return new_data

api.register_blueprint(blp)
