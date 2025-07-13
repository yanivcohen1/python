from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS, cross_origin

from flask_restful import Api
from flaskr.tools.flask_mongo.resources.errors import errors
from flaskr.tools.flask_mongo.database.db import initialize_db

app = Flask(__name__)
app.config.from_envvar('ENV_FILE_LOCATION') # read from config file
print("SECRET_KEY:" + app.config["JWT_SECRET_KEY"]) # read from config file a key
print("config read all keys:")
print(app.config) # read from config file all keys
mail = Mail(app)

api = Api(app, errors=errors)
CORS(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

initialize_db(app)

# imports requiring app and mail
from flaskr.tools.flask_mongo.resources.routes import initialize_routes
initialize_routes(api)

# not from restAPI
# @app.get('/test-app')
# @app.post('/test-app')
@app.route('/test-app', methods=['GET'])
def testApp():
    # return jsonify({'name': 'alice',
    #                'email': 'alice@outlook.com'})
    # query = Movie.objects()
    from flaskr.tools.flask_mongo.database.models import Movie
    movies:list[Movie] = Movie.objects() # pylint: disable=no-member
    print(movies[0].embeds[0].name) # yan1
    print(movies[1].embeds[0].name) # yan2
    return movies.to_json()

if __name__ == "__main__":
    # with app.app_context():
    #     # Create the tables
    #     db.create_all()

    #     # Insert initial users
    #     user1 = User(id=1, username="yaniv",
    #                  password=bcrypt.generate_password_hash("yaniv_P").decode('utf-8'))
    #     user2 = User(id=2, username="yaniv2",
    #                  password=bcrypt.generate_password_hash("yaniv2_P").decode('utf-8'))
    #     user3 = User(id=3, username="yaniv3",
    #                  password=bcrypt.generate_password_hash("yaniv3_P").decode('utf-8'))
    #     db.session.add_all([user1, user2, user3])
    #     db.session.commit()

    #     # Insert initial data
    #     author1 = Author(id=1, name="F. Scott Fitzgerald")
    #     author2 = Author(id=2, name="George Orwell")
    #     author3 = Author(id=3, name="Jane Austen")

    #     db.session.add_all([author1, author2, author3])
    #     db.session.commit()

    #     book1 = Book(id=1, title="The Great Gatsby", author_id=author1.id)
    #     book2 = Book(id=2, title="1984", author_id=author2.id)
    #     book3 = Book(id=3, title="Pride and Prejudice", author_id=author3.id)

    #     db.session.add_all([book1, book2, book3])
    #     db.session.commit()

    app.run(debug=True, port=5000)
