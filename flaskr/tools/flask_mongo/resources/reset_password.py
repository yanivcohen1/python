import datetime

from flaskr.tools.flask_mongo.resources.errors import (BadTokenError, EmailDoesnotExistsError,
                    InternalServerError, SchemaValidationError)
from jwt.exceptions import (DecodeError, ExpiredSignatureError,
                            InvalidTokenError)
from flask import render_template, request
from flask_jwt_extended import create_access_token, decode_token
from flask_restful import Resource
from flaskr.tools.flask_mongo.database.models import User
from flaskr.tools.flask_mongo.services.mail_service import send_email


class ForgotPassword(Resource):
    def post(self):
        url = request.host_url + 'reset/'
        try:
            body = request.get_json()
            email = body.get('email')
            if not email:
                raise SchemaValidationError
            # pylint: disable=no-member
            user = User.objects.get(email=email)
            if not user:
                raise EmailDoesnotExistsError

            expires = datetime.timedelta(hours=24)
            reset_token = create_access_token(str(user.id), expires_delta=expires)

            return send_email('[Movie-bag] Reset Your Password',
                              sender='support@movie-bag.com',
                              recipients=[user.email],
                              text_body=render_template('email/reset_password.txt',
                                                        url=url + reset_token),
                              html_body=render_template('email/reset_password.html',
                                                        url=url + reset_token))
        except SchemaValidationError as exc:
            raise SchemaValidationError from exc
        except EmailDoesnotExistsError as exc:
            raise EmailDoesnotExistsError from exc
        except Exception as e:
            raise InternalServerError from e


class ResetPassword(Resource):
    def post(self):
        url = request.host_url + 'reset/'
        try:
            body = request.get_json()
            reset_token = body.get('reset_token')
            password = body.get('password')

            if not reset_token or not password:
                raise SchemaValidationError

            user_id = decode_token(reset_token)['identity']
            # pylint: disable=no-member
            user = User.objects.get(id=user_id)

            user.modify(password=password)
            user.hash_password()
            user.save()

            return send_email('[Movie-bag] Password reset successful',
                              sender='support@movie-bag.com',
                              recipients=[user.email],
                              text_body='Password reset was successful',
                              html_body='<p>Password reset was successful</p>')

        except SchemaValidationError as exc:
            raise SchemaValidationError from exc
        except ExpiredSignatureError as exc:
            raise ExpiredSignatureError from exc
        except (DecodeError, InvalidTokenError):
            raise BadTokenError from exc
        except Exception as e:
            raise InternalServerError from e
