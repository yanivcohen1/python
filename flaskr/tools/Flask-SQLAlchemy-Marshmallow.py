# install "flask", "flask-marshmallow", "flask-sqlalchemy", "marshmallow-sqlalchemy"
import os
import json
from dataclasses import dataclass
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
from sqlalchemy.sql import text

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ \
                os.path.join(basedir, 'db.sqlite3')

db = SQLAlchemy(app)
# ma = Marshmallow(app)

@dataclass
class NoteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(255))

    # def __init__(self, title, content):
    #     self.title = title
    #     self.content = content

# https://github.com/marshmallow-code/marshmallow-sqlalchemy#generate-marshmallow-schemas
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

class NoteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = NoteModel
        include_relationships = True
        load_instance = True
# class NoteSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = NoteModel

note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)

# inner join #######################################
# import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref

# engine = sa.create_engine("sqlite:///:memory:")
# session = scoped_session(sessionmaker(bind=app.app_context()))
# Base = declarative_base()


class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return "<Author(name={self.name!r})>".format(self=self)


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"))
    author = relationship("Author", backref=backref("books"))


class AuthorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Author
        include_relationships = True
        load_instance = True


class BookSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Book
        include_fk = True
        load_instance = True

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/note/')
def note_list():
    all_notes = NoteModel.query.all()
    return jsonify(notes_schema.dump(all_notes))

@app.route('/note2/')
def note_list2():
    # all_notes = NoteModel.query.all()
    output = db.session.execute(text("SELECT * FROM note_model;"))
    results = output.fetchall()
    return json.dumps(results, default=str)

@app.route('/note/', methods=['POST'])
def create_note():
    title = request.json.get('title', '')
    content = request.json.get('content', '')
    note = NoteModel(title=title, content=content)
    db.session.add(note)
    db.session.commit()
    return note_schema.dumps(note)

@app.route('/note2/', methods=['POST'])
def create_note2():
    note = note_schema.load(request.json, session=db.session)
    db.session.add(note)
    db.session.commit()
    return note_schema.dumps(note)

@app.route('/note/<int:note_id>/', methods=["GET"])
def note_detail(note_id):
    note = NoteModel.query.get(note_id)
    return note_schema.dumps(note)


@app.route('/note/<int:note_id>/', methods=['PATCH'])
def update_note(note_id):
    title = request.json.get('title', '')
    content = request.json.get('content', '')

    note = NoteModel.query.get(note_id)

    note.title = title
    note.content = content

    db.session.add(note)
    db.session.commit()

    return note_schema.dumps(note)


@app.route('/note/<int:note_id>/', methods=["DELETE"])
def delete_note(note_id):
    note = NoteModel.query.get(note_id)

    db.session.delete(note)
    db.session.commit()

    return note_schema.dumps(note)

@app.route('/author/')
def create_author():
    author = Author(name="Chuck Paluhniuk")
    author_schema = AuthorSchema()
    book = Book(title="Fight Club", author=author)
    book_schema = BookSchema()

    db.session.add(author)
    db.session.add(book)
    db.session.commit()

    dump_author = author_schema.dump(Author.query.get(author.id))
    # dump_author = {'id': 1, 'name': 'Chuck Paluhniuk', 'books': [1]}
    dump_book = book_schema.dump(Book.query.get(book.id))
    # dump_book = {'id': 3, 'title': 'Fight Club', 'author_id': 3}
    load_author = author_schema.load(dump_author, session=db.session)
    load_book = book_schema.load(dump_book, session=db.session)
    # print(load_data)
    return book_schema.dump(load_book)

@app.route('/authors/')
def get_all_authors():
    authors = Author.query.all()
    return AuthorSchema(many=True).dump(authors)

@app.route('/books/')
def get_all_books():
    books = Book.query.all()
    autor = books[0].author
    return BookSchema(many=True).dump(books)

@app.route('/first_autor/')
def get_first_autor():
    books = Book.query.all()
    autor = books[0].author
    return AuthorSchema().dump(autor)

if __name__ == '__main__':
    # run once to create DB in file db.sqlite3
    with app.app_context():
        db.create_all()
    app.run(debug=True)
