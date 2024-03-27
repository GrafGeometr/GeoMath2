from test import db
from test.base_test_case import BaseTestCase


class TestUser(BaseTestCase):
    def test_create_user(self):
        # print("test_create_user")
        from app.db_classes.user import User

        user = User(name="test").add()

        self.assertEqual(user.name, "test")
