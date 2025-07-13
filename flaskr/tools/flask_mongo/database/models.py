from enum import Enum
from typing import List
from flask_bcrypt import generate_password_hash, check_password_hash
from flaskr.tools.flask_mongo.database.db import db
from mongoengine import EmbeddedDocument, Document, StringField, ListField, EmbeddedDocumentField, ReferenceField, EmailField, EnumField, CASCADE, PULL

class Embed(EmbeddedDocument):
    name: str = StringField(default='yan')
    value: str = StringField(default='con')

class Movie(db.Document):
    name: str = StringField(required=True, unique=True)
    casts: list[str] = ListField(StringField(), required=True)
    genres: list[str]  = ListField(StringField(), required=True)
    #find=Movie.objects(embeds__match={ "name": "xxx", "value": "xxx" }) # and query in embedded fields
    embeds: list[Embed] = ListField(EmbeddedDocumentField(Embed))
    added_by = ReferenceField('User')

class Role(Enum):
    USER = 'user'
    SUPER_USER = 'super_user'
    ADMIN = 'admin'

class User(db.Document):
    email: str = EmailField(required=True, unique=True)
    password: str = StringField(required=True, min_length=6)
    role: Role = EnumField(Role, default=Role.USER)
    movies: list[Movie] = ListField(ReferenceField('Movie', reverse_delete_rule=PULL))

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

User.register_delete_rule(Movie, 'added_by', CASCADE)
