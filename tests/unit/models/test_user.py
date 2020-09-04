from tests.unit.unit_base_test import UnitBaseTest
from models.user import UserModel


class UserTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel('Test Name', 'password123')
        self.assertEqual(user.username, 'Test Name', 'User name does not match constructor argument')
        self.assertEqual(user.password, 'password123', 'Password does not match constructor argument')