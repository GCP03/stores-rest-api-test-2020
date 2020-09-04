from models.user import UserModel
from tests.base_test import BaseTest


class UserTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            user = UserModel('test', 'abcd')
            # user instance created but not added to db
            self.assertIsNone(UserModel.find_by_user_name('test'))
            self.assertIsNone(UserModel.find_by_id(1))

            user.save_to_db()

            self.assertIsNotNone(UserModel.find_by_user_name('test'))
            self.assertIsNotNone(UserModel.find_by_id(1))
