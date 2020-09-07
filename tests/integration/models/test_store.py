from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store_items_empty(self):
        store = StoreModel('test')
        self.assertListEqual(store.items.all(), [],
                             'The stores item length was not 0 even though no items were added')

    def test_crud(self):
        with self.app_context():
            store = StoreModel('Test')
            self.assertIsNone(StoreModel.find_by_name('Test'))

            store.save_to_db()
            self.assertIsNotNone(StoreModel.find_by_name('Test'))

            store.delete_from_db()
            self.assertIsNone(StoreModel.find_by_name('Test'))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('Test')
            item = ItemModel('Test Item1', 19.99, 1)
            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, 'Test Item1')

    def test_store_json(self):
        store = StoreModel('Test')
        expected_json = {'id': None,
                         'name': 'Test',
                         'items': []
                        }
        self.assertDictEqual(store.json(), expected_json,
                             'Store JSON value is not as expected')

    def test_store_json_multiple_items(self):
        # app_context needed since we are adding to db
        with self.app_context():
            store = StoreModel('Test')
            item = ItemModel('Test Item1', 19.99, 1)
            store.save_to_db()
            item.save_to_db()
            expected_json = {'id': 1,
                             'name': 'Test',
                             'items': [{'name': 'Test Item1', 'price': 19.99}]
                             }
            self.assertDictEqual(store.json(), expected_json)
