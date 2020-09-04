from models.store import StoreModel
from tests.unit.unit_base_test import UnitBaseTest


class StoreTest(UnitBaseTest):
    def test_create_store(self):
        store = StoreModel('Test')
        self.assertEqual(store.name, 'Test',
                         'Store name after creation does not match constructor argument')
