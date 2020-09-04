from models.user import UserModel
from tests.base_test import BaseTest
import json


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/register', data={'username': 'test',
                                                         'password': 'abcd',
                                                         }
                                      )
                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_user_name('test'))
                self.assertDictEqual({'Message': 'User has been added'}, json.loads(response.data))

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/register', data={'username': 'test',
                                                         'password': 'abcd',
                                                         }
                                      )
                auth_response = client.post('/auth', data=json.dumps({'username': 'test', 'password': 'abcd'}),
                                           headers={'Content-Type': 'application/json'}
                                           )
                self.assertIn('access_token', json.loads(auth_response.data).keys())

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': 'abcd'})
                response = client.post('/register', data={'username': 'test', 'password': 'abcd'})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'Message': 'A user with that username already exists'},
                                     json.loads(response.data))