import unittest

from flaskr.tools.flask_mongo.app import app
from flaskr.tools.flask_mongo.database.db import db


class BaseCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        # pylint: disable=no-member
        self.db = db.get_db()

    def tearDown(self):
        # Delete Database collections after the test is complete
        for collection in self.db.list_collection_names():
            self.db.drop_collection(collection)
