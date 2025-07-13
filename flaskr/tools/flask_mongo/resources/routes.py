from flaskr.tools.flask_mongo.resources.movie import MoviesApi, MovieApi, MoviesApiQuery
from flaskr.tools.flask_mongo.resources.auth import SignupApi, LoginApi
from flaskr.tools.flask_mongo.resources.reset_password import ForgotPassword, ResetPassword


def initialize_routes(api):
    api.add_resource(MoviesApi, '/api/movies')
    api.add_resource(MovieApi, '/api/movies/<id>')
    api.add_resource(MoviesApiQuery, '/api/movie')

    api.add_resource(SignupApi, '/api/auth/signup')
    api.add_resource(LoginApi, '/api/auth/login')

    api.add_resource(ForgotPassword, '/api/auth/forgot')
    api.add_resource(ResetPassword, '/api/auth/reset')
