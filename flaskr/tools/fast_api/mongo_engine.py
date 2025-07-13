from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from mongoengine import Document, StringField, ListField, EmbeddedDocument, EmbeddedDocumentField, connect

# Initialize FastAPI
app = FastAPI()

# MongoDB setup with MongoEngine
connect("bookstore", host="mongodb://localhost:27017/bookstore")

# MongoEngine models
class Comment(EmbeddedDocument):
    text = StringField(required=True)

class Author(Document):
    meta = {"collection": "authors"}
    id = StringField(required=False, primary_key=True, alias="_id")
    name = StringField(required=True)
    comments = ListField(EmbeddedDocumentField(Comment))

class Book(Document):
    meta = {"collection": "books"}
    id = StringField(required=False, primary_key=True, alias="_id")
    title = StringField(required=True)
    author_id = StringField(required=True)

# Route to find books by author's name
@app.get("/books/by_author/{author_name}", response_model=List[Book])
async def get_books_by_author(author_name: str):
    # pylint: disable=no-member
    author = Author.objects(name=author_name).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    # pylint: disable=no-member
    books: List[Book] = Book.objects(author_id=str(author.id))
    return [Book(**book.to_mongo().to_dict()) for book in books]

# Route to add an author (for testing purposes)
@app.post("/authors", response_model=Author)
async def create_author(author: Author):
    new_author = Author(
        id=author.id,
        name=author.name,
        comments=[Comment(text=comment.text) for comment in author.comments]
    )
    new_author.save()
    return new_author

# Route to add a book (for testing purposes)
@app.post("/books", response_model=Book)
async def create_book(book: Book):
    new_book = Book(
        id=book.id,
        title=book.title,
        author_id=book.author_id
    )
    new_book.save()
    return new_book
