from typing import Optional
from flask import Response, request
from flask_jwt_extended import create_access_token
from flaskr.tools.flask_mongo.database.models import User
from flask_restful import Resource
import datetime
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist
from flaskr.tools.flask_mongo.resources.errors import SchemaValidationError, EmailAlreadyExistsError, UnauthorizedError, \
InternalServerError

from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt
from flask_jwt_extended import verify_jwt_in_request
from flaskr.tools.flask_mongo.database.models import Role
from mongoengine import Document

class SignupApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            user: User =  User(**body)
            user.hash_password()
            user.save()
            id = user.pk
            return {'id': str(id)}, 200
        except FieldDoesNotExist:
            raise SchemaValidationError
        except NotUniqueError:
            raise EmailAlreadyExistsError
        except Exception as e:
            raise InternalServerError

class LoginApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            # pylint: disable=no-member
            user: User = User.objects.get(email=body.get('email'))
            authorized = user.check_password(body.get('password'))
            if not authorized:
                raise UnauthorizedError

            expires = datetime.timedelta(days=7)
            admin = False
            if user.role == Role.ADMIN: admin = True
            access_token = create_access_token(identity=str(user.id), expires_delta=expires,
                                               additional_claims={"is_administrator": admin}) # True
            return {'token': access_token}, 200
        except (UnauthorizedError, DoesNotExist):
            raise UnauthorizedError
        except Exception as e:
            raise InternalServerError

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["is_administrator"]:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Admins only!"), 403

        return decorator

    return wrapper
