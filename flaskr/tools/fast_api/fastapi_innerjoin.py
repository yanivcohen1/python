from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, Session
from sqlalchemy import create_engine
from passlib.context import CryptContext
import jwt
from pydantic import BaseModel
from typing import List, Optional

DATABASE_URL = "mysql+pymysql://root:yanivc77@localhost/alchemy"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# Pydantic Schemas
class AuthorBase(BaseModel):
    name: str

class AuthorCreate(AuthorBase):
    pass

class AuthorResponse(AuthorBase):
    id: int
    class Config:
        orm_mode = True

class BookBase(BaseModel):
    title: str
    author_id: int

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int
    author: Optional[AuthorResponse]
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String) # hashed_password

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    books = relationship("Book", back_populates="author")

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="books")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/register/")
def register(username: str, password: str, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(password)
    user = User(username=username, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered successfully"}

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print(f"Received login request: username={form_data.username}, password={form_data.password}")  # Debugging
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
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
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return {"username": user.username}
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

@app.post("/books/", response_model=BookResponse)
def create_book(title: str, author_id: int, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    book = Book(title=title, author_id=author_id)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

@app.get("/books/", response_model=List[BookResponse])
def read_books(request: Request, response: Response, db: Session = Depends(get_db)):
    try:
        custom_header = request.headers.get('Custom-Header')
        response.headers['Custom-Header'] = custom_header + '-Response'
    except: pass
    return db.query(Book).all()

@app.get("/books/{book_id}", response_model=BookResponse)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.get("/books/by_author/{author_id}", response_model=List[BookResponse])
def find_books_by_author(author_id: int, db: Session = Depends(get_db)):
    return db.query(Book).filter(Book.author_id == author_id).all()

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=5000) # host="0.0.0.0"

# for swagger API http://127.0.0.1:5000/docs#/
# for fastAPI http://127.0.0.1:5000/redoc

def create_DB():
    ...
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
