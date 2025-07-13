from flask_mongoengine import MongoEngine

db = MongoEngine()

def initialize_db(app):
    """initialize db."""
    db.init_app(app)
