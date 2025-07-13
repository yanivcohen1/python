from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, SQLModel, create_engine, Session, select, Relationship
from passlib.context import CryptContext
from sqlalchemy import text
from sqlalchemy.orm import joinedload
import jwt
from pydantic import BaseModel

DATABASE_URL = "mysql+pymysql://root:yanivc77@localhost/sqlmodel"
engine = create_engine(DATABASE_URL)
SessionLocal = Session(engine)

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

# SQLModel models
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str # hashed_password

class Author(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    books: List["Book"] = Relationship(back_populates="author")

class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    author_id: int = Field(foreign_key="author.id")
    author: Optional[Author] = Relationship(back_populates="books")

SQLModel.metadata.create_all(engine)

class BookResponse(BaseModel):
    id: int
    title: str
    author: Author

    class Config:
        orm_mode = True
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

def get_db():
    with Session(engine) as db:
        try:
            yield db
        finally:
            db.close()

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
def register(username: str, password: str, db: Session = Depends(get_db)):
    password = get_password_hash(password)
    user = User(username=username, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered successfully"}

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/logout/")
def logout():
    return {"message": "User logged out successfully"}

@app.get("/get_user_name")
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        user = db.exec(select(User).where(User.username == username)).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return {"username": user.username}
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

@app.get("/protected")
def protected(token: str = Depends(oauth2_scheme)):
    return "protected content"

@app.post("/books/", response_model=Book)
def create_book(book: Book, db: Session = Depends(get_db)):
    author = db.exec(select(Author).where(Author.id == book.author_id)).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    new_book = Book(title=book.title, author_id=book.author_id)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@app.get("/books/", response_model=List[BookResponse])
def read_books(request: Request, response: Response, db: Session = Depends(get_db)):
    try:
        custom_header = request.headers.get('Custom-Header')
        response.headers['Custom-Header'] = custom_header + '-Response'
    except: pass
    return db.exec(select(Book)).all()

@app.get("/books/{book_id}", response_model=Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = db.exec(select(Book).where(Book.id == book_id)).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.get("/books/by_author/{author_id}", response_model=List[Book])
def find_books_by_author(author_id: int, db: Session = Depends(get_db)):
    return db.exec(select(Book).where(Book.author_id == author_id)).all()

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.exec(select(Book).where(Book.id == book_id)).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}

def run_native_query(query: str):
    with Session(engine) as session:
        result = session.exec(text(query))
    return result.all()

def get_pagination_resoult(query, page: int = 1, page_size: int = 10):
    offset = (page - 1) * page_size
    statement = query.offset(offset).limit(page_size)
    with Session(engine) as db:
        result = db.exec(statement).all()
    return result

def create_DB():
    with Session(engine) as db:
        # Create the tables
        # SQLModel.metadata.create_all(engine)

        # Insert initial users
        user1 = User(id=1, username="yaniv",
                      hashed_password=get_password_hash("yaniv_P"))
        user2 = User(id=2, username="yaniv2",
                      hashed_password=get_password_hash("yaniv2_P"))
        user3 = User(id=3, username="yaniv3",
                      hashed_password=get_password_hash("yaniv3_P"))
        db.add_all([user1, user2, user3])
        db.commit()

        # Insert initial data
        author1 = Author(id=1, name="F. Scott Fitzgerald")
        author2 = Author(id=2, name="George Orwell")
        author3 = Author(id=3, name="Jane Austen")

        db.add_all([author1, author2, author3])
        db.commit()

        book1 = Book(id=1, title="The Great Gatsby", author_id=author1.id)
        book2 = Book(id=2, title="1984", author_id=author2.id)
        book3 = Book(id=3, title="Pride and Prejudice", author_id=author3.id)

        db.add_all([book1, book2, book3])
        db.commit()

def run_native_query_example():
    # Example usage
    query = "SELECT `book`.`title`, `author`.`name`, `author`.`id` FROM `book` , `author`"
    results = run_native_query(query)
    for row in results:
        print(row)

def run_paganation():
    query = select(Book) # .where(Book.id == book_id)
    books = get_pagination_resoult(query, 1, 10)
    for book in books:
        print(book)

if __name__ == "__main__":
    # create_DB()
    # run_native_query_example()
    # run_paganation()
    import uvicorn
    uvicorn.run(app, port=5000) # host="0.0.0.0"

# for swagger API http://127.0.0.1:5000/docs#/
# for fastAPI http://127.0.0.1:5000/redoc
