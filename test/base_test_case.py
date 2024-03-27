import os
import unittest

from test import create_test_app, db


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        # remove file if exists
        if os.path.exists("database/test.db"):
            os.remove("database/test.db")
        self.app = create_test_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
