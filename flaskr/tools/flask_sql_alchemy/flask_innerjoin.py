import functools
from typing import List
from flask import Flask, jsonify, request, make_response, g, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required # ,current_user
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from marshmallow import fields, ValidationError
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@localhost/db_name'
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:yanivc77@localhost/alchemy"
)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Use an in-memory SQLite database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'your_secret_key' # for login manager pass incrypt
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key' # for jwf token
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
cors = CORS(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
api = Api(app)

# Define the models
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(50), unique=True, nullable=False)
    password: str = db.Column(db.String(255), nullable=False)

class Author(db.Model):
    __tablename__ = "authors"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(50), nullable=False)

class Book(db.Model):
    __tablename__ = "books"
    id: int = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.String(100), nullable=False)
    author_id: int = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=False)
    author = db.relationship("Author", backref=db.backref("books", lazy=True))


# Define the Marshmallow schemas
class AuthorSchema(SQLAlchemySchema):
    class Meta:
        model = Author

    id = auto_field()
    name = auto_field()


class BookSchema(SQLAlchemySchema):
    class Meta:
        model = Book

    id = auto_field()
    title = auto_field()
    author_id = auto_field()
    author = fields.Nested(AuthorSchema)


author_schema = AuthorSchema()
book_schema = BookSchema()
books_schema = BookSchema(many=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    password = data['password']
    user: User = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({'access_token': access_token})
    return jsonify({'message': 'Invalid username or password'}), 401

###################################
@app.errorhandler(404)
def not_found(error=None):
    if error is None:
        message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
        }
    else:
        message = {
            'status': 404,
            'message': error,
        }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})

def admin_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        # autorization = request.headers.get('Autorization')
        user_id = get_jwt_identity()
        user: User = load_user(user_id)
        if user.username is None:
            return not_found("login required")
        else:
            if user.username != 'yaniv':
                return not_found("Only admin can access this page")
        return view(**kwargs)

    return wrapped_view

@app.route('/get_user_id')
@jwt_required()
@admin_required
def get_user_id():
    user_id = get_jwt_identity()
    return f"user Id is - {user_id}"

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    user: User = load_user(user_id)
    return jsonify({'message': f'Hello, {user.username}! This is a protected route.'})

# Perform an inner join query
@app.route("/books_with_authors") # , methods=["GET"]
def get_books_with_authors():
    # Perform an inner join query
    result = db.session.query(Book).join(Author).all()
    books_with_authors = books_schema.dump(result)
    return jsonify(books_with_authors)


@app.route("/add_book", methods=["POST"])
def add_book():
    try:
        data = request.get_json()
        book_data = book_schema.load(data)
        new_book = Book(title=book_data["title"], author_id=book_data["author_id"])
        db.session.add(new_book)
        db.session.commit()
        return jsonify(book_schema.dump(new_book)), 201
    except ValidationError as err:
        return jsonify(err.messages), 400

@app.route('/get_book/<int:book_id>') # http://127.0.0.1:5000/get_book/2
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify(book_schema.dump(book))

@app.route('/get_book2') # http://127.0.0.1:5000/get_book2?book_id=2
def get_book2():
    book_id = request.args.get('book_id', type=int)
    if book_id is None:
        return jsonify({'error': 'book_id query parameter is required'}), 400
    book = Book.query.get_or_404(book_id)
    return jsonify(book_schema.dump(book))

@app.route('/find_book_by_name')# GET /find_book_by_name?book_name=The Great Gatsby
def find_book_by_name():
    book_name = request.args.get('book_name')
    if book_name is None:
        return jsonify({'error': 'book_name query parameter is required'}), 400
    book = Book.query.filter_by(title=book_name).first_or_404()
    return jsonify(book_schema.dump(book))


class FindBooksByAuthorNameResource(Resource):
    # GET /api/find_books_by_author_name?author_name=F. Scott Fitzgerald
    # @app.route('/find_books_by_author_name')
    def get(self):
        custom_header = request.headers.get('Custom-Header')
        # print(f'Custom-Header: {custom_header}')
        author_name = request.args.get("author_name")
        if author_name is None:
            return jsonify({"error": "author_name query parameter is required"}), 400
        author: Author = Author.query.filter_by(name=author_name).first_or_404()
        books = Book.query.filter_by(author_id=author.id).all()
        response = make_response(jsonify(books_schema.dump(books)))
        response.headers['Custom-Header'] = custom_header + '-Response'
        # response.headers['Header-Two'] = 'Value2'
        return response


class FindBooksTitleByAuthorNameResource(Resource):
    # GET /api/find_books_title_by_author_name?author_name=F. Scott Fitzgerald
    # @app.route('/find_books_title_by_author_name')
    def get(self):
        author_name = request.args.get("author_name")
        if author_name is None:
            return jsonify({"error": "author_name query parameter is required"}), 400
        author: Author = Author.query.filter_by(name=author_name).first_or_404()
        books: List[Book] = Book.query.filter_by(author_id=author.id).all()
        # return jsonify(book_schema.dump(books, many=True))
        book_titles = [book.title for book in books]
        return jsonify({"book_titles": book_titles})


# all Resources
api.add_resource(FindBooksByAuthorNameResource, '/api/find_books_by_author_name')
api.add_resource(FindBooksTitleByAuthorNameResource, '/api/find_books_title_by_author_name')

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
