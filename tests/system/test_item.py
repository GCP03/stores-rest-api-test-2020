from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
from tests.base_test import BaseTest
import json


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()

        with self.app() as client:
            with self.app_context():
                UserModel('test', 'abcd').save_to_db()
                auth_response = client.post('/auth', data=json.dumps({'username': 'test', 'password': 'abcd'}),
                                           headers={'Content-Type': 'application/json'}
                                           )
                auth_token = json.loads(auth_response.data)['access_token']
                self.access_token = f'JWT {auth_token}'

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                # StoreModel('test').save_to_db()
                # ItemModel('test item', 19.99, 1).save_to_db()
                response = client.get('/item/test item')

                self.assertEqual(401, response.status_code)

                expected = {'message': 'Could not authorize. Did you include a valid Authorization header?'}
                self.assertDictEqual(expected, json.loads(response.data))

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                # Moved to setUp method
                # UserModel('test', 'abcd').save_to_db()
                # auth_response = client.post('/auth', data=json.dumps({'username': 'test', 'password': 'abcd'}),
                #                            headers={'Content-Type': 'application/json'}
                #                            )
                # auth_token = json.loads(auth_response.data)['access_token']
                # header = {'Authorization': f'JWT {auth_token}'}

                response = client.get('/item/test', headers={'Authorization': self.access_token})
                self.assertEqual(404, response.status_code)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test item', 19.99, 1).save_to_db()
                response = client.get('/item/test item', headers={'Authorization': self.access_token})
                self.assertEqual(200, response.status_code)

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test item', 19.99, 1).save_to_db()
                response = client.delete('/item/test item', headers={'Authorization': self.access_token})
                self.assertEqual(200, response.status_code)
                expected = {'message': 'Item deleted'}
                self.assertDictEqual(expected, json.loads(response.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                response = client.post('/item/test item', headers={'Authorization': self.access_token},
                                       data={'price': 19.99, 'store_id': 1})
                self.assertEqual(201, response.status_code)
                expected = {'name': 'test item', 'price': 19.99}
                self.assertDictEqual(expected, json.loads(response.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test item', 19.99, 1).save_to_db()
                response = client.post('/item/test item', headers={'Authorization': self.access_token},
                                                                   data={'price': 19.99, 'store_id': 1})
                self.assertEqual(400, response.status_code)
                expected = {'message': "An item with name 'test item' already exists."}
                self.assertDictEqual(expected, json.loads(response.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                response = client.put('/item/test item', data={'price': 19.99, 'store_id': 1})
                self.assertEqual(200, response.status_code)
                expected = {'name': 'test item', 'price': 19.99}
                self.assertDictEqual(expected, json.loads(response.data))

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test item', 19.99, 1)
                # client.put('/item/test item', data={'price': 19.99, 'store_id': 1})
                response = client.put('/item/test item', data={'price': 5.00, 'store_id': 1})
                self.assertEqual(200, response.status_code)
                expected = {'name': 'test item', 'price': 5.00}
                self.assertDictEqual(expected, json.loads(response.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test item', 19.99, 1).save_to_db()
                response = client.get('/items')
                self.assertEqual(200, response.status_code)

                expected = {'items': [{'name': 'test item', 'price': 19.99}]}
                self.assertDictEqual(expected, json.loads(response.data))

    def test_multiple_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test item', 19.99, 1).save_to_db()
                ItemModel('test item2', 5.75, 1).save_to_db()
                response = client.get('/items')
                self.assertEqual(200, response.status_code)

                expected = {'items': [{'name': 'test item', 'price': 19.99},
                                      {'name': 'test item2', 'price': 5.75}]}
                self.assertDictEqual(expected, json.loads(response.data))
