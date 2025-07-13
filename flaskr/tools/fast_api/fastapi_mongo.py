from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
import jwt
from pymongo import MongoClient
from pymongo.cursor import Cursor
from pydantic import BaseModel, Field
from bson import ObjectId

DATABASE_URL = "mongodb://localhost:27017"
DATABASE_NAME = "fastapi"
client = MongoClient(DATABASE_URL)
db = client[DATABASE_NAME]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List of allowed origins (use ["*"] to allow all)
    allow_credentials=True,  # Allow sending cookies (for authentication)
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Pydantic models
class User(BaseModel):
    id: Optional[str] = Field(None, alias='_id')
    username: str
    hashed_password: str

class Comment(BaseModel):
    content: str

class Author(BaseModel):
    id: Optional[str] = Field(None, alias='_id')
    name: str
    comments: List[Comment] = []

class Book(BaseModel):
    id: Optional[str] = Field(None, alias='_id')
    title: str
    author_id: str

class BookResponse(BaseModel):
    id: Optional[str]
    title: str
    author: Author

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

def from_dict(cls, data: dict):
    # Convert _id to a string if it exists
    if '_id' in data:
        data['_id'] = str(data['_id'])
        data['id'] = str(data['_id'])
    return cls(**data)

def verify_password(plain_password, password):
    return pwd_context.verify(plain_password, password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/register/")
def register(username: str, password: str):
    hashed_password = get_password_hash(password)
    user = {"username": username, "hashed_password": hashed_password}
    db.users.insert_one(user)
    return {"message": "User registered successfully"}

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.users.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/logout/")
def logout():
    return {"message": "User logged out successfully"}

@app.get("/get_user_name")
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        user = db.users.find_one({"username": username})
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return {"username": user["username"]}
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

@app.get("/protected")
def protected(token: str = Depends(oauth2_scheme)):
    return "protected content"

@app.post("/books/", response_model=Book)
def create_book(book: Book):
    author = db.authors.find_one({"_id": book.author_id})
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    # new_book = {"title": book.title, "author_id": book.author_id}
    result = db.books.insert_one(book.dict(by_alias=True))
    return result.inserted_id

@app.get("/books/", response_model=List[BookResponse])
def read_books(request: Request, response: Response):
    try:
        custom_header = request.headers.get('Custom-Header')
        response.headers['Custom-Header'] = custom_header + '-Response'
    except: pass
    book_dicts = list(db.books.find())
    books = [from_dict(Book, book_dict) for book_dict in book_dicts]
    return [BookResponse(id=book.id, title=book.title, author=from_dict(Author, db.authors.find_one({"_id": ObjectId(book.author_id)}))) for book in books]

@app.get("/books/{book_id}", response_model=Book)
def read_book(book_id: str):
    book = db.books.find_one({"_id": book_id})
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.get("/books/by_author/{author_id}", response_model=List[Book])
def find_books_by_author(author_id: str):
    books = db.books.find({"author_id": author_id})
    return list(books)

@app.delete("/books/{book_id}")
def delete_book(book_id: str):
    book = db.books.find_one({"_id": book_id})
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.books.delete_one({"_id": book_id})
    return {"message": "Book deleted successfully"}

@app.get("/find_authors_by_comment/{comment}", response_model=Author)
def find_authors_by_comment_text(comment: str):
    authors = db.authors.find({"comments.content": comment})
    # authors = [from_dict(Author, author) for author in authors]
    return list(authors)

# Function to get paginated results
def get_paginated_results(page: int, page_size: int, cursor: Cursor):
    skip = (page - 1) * page_size
    results = cursor.skip(skip).limit(page_size)
    return list(results)

def create_DB():
    # Insert initial users
    user1 = User(username= "yaniv", hashed_password = get_password_hash("yaniv_P")).dict()
    user2 = User(username= "yaniv2", hashed_password = get_password_hash("yaniv2_P")).dict()
    user3 = User(username= "yaniv3", hashed_password = get_password_hash("yaniv3_P")).dict()
    db.users.insert_many([user1, user2, user3])

    comment1 = Comment(content="comment1").dict()
    comment2 = Comment(content="comment2").dict()
    comment3 = Comment(content="comment3").dict()

    # Insert initial authors with embedded Comments
    author1 = Author(name="F. Scott Fitzgerald", comments=[comment1]).dict()
    author2 = Author(name="George Orwell", comments=[comment2]).dict()
    author3 = Author(name="Jane Austen", comments=[comment3]).dict()
    # author2 = {"name": "George Orwell"}
    # author3 = {"name": "Jane Austen"}
    db.authors.insert_many([author1, author2, author3])

    # Insert initial books
    book1 = Book(title= "The Great Gatsby", author_id= str(author1["_id"])).dict()
    book2 = Book(title= "1984", author_id= str(author2["_id"])).dict()
    book3 = Book(title= "Pride and Prejudice", author_id= str(author3["_id"])).dict()
    db.books.insert_many([book1, book2, book3])

def run_native_query():
    # Find all users whose username starts with 'yaniv' and sort by username
    users_collections = db["users"]
    users_ = users_collections.find(
      {"username": {"$regex": "^yaniv"}},
      {"hashed_password": 0} # exclude hashed_password
    ).sort("username", 1)
    users = get_paginated_results(1, 10, users_)
    for user in users:
        print(user)


if __name__ == "__main__":
    # create_DB()
    # run_native_query()
    # print("authors:", find_authors_by_comment_text("comment1"))
    import uvicorn
    uvicorn.run(app, port=5000) # host="0.0.0.0"

# for swagger API http://127.0.0.1:5000/docs#/
# for fastAPI http://127.0.0.1:5000/redoc
