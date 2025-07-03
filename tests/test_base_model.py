#!/usr/bin/python3
""" test base module """


import unittest
from models.base_model import BaseModel
import uuid
from datetime import datetime
from unittest.mock import patch


class TestBaseModel(unittest.TestCase):
    """
    test base class
    """
    def test_id_existence(self):
        base = BaseModel()
        self.assertTrue(hasattr(base, "id"))

    def test_id_type(self):
        base = BaseModel()
        self.assertIsInstance(base.id, str)

    def test_valid_uuid(self):
        try:
            base = BaseModel()
            uuid_obj = uuid.UUID(base.id)
        except ValueError:
            self.fail("id is not a valid UUID")

    def test_unique_id(self):
        base1 = BaseModel()
        base2 = BaseModel()
        self.assertNotEqual(base1, base2)

    def test_created_at_type(self):
        base = BaseModel()
        self.assertIsInstance(base.created_at, datetime)

    def test_updated_at_type(self):
        base = BaseModel()
        self.assertIsInstance(base.updated_at, datetime)

    @patch('models.base_model.datetime')
    def test_str_method(self, mock_datetime):
        # Setup fixed time and UUID
        fixed_uuid = "12345678-1234-5678-1234-567812345678"
        fixed_time = datetime(2024, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = fixed_time

        with patch('uuid.uuid4', return_value=fixed_uuid):
            obj = BaseModel()

            # Expected output (match key order exactly)
            expected_dict = {
                'id': fixed_uuid,
                'created_at': fixed_time,
                'updated_at': fixed_time,
            }
            expected_str = f"[BaseModel] ({fixed_uuid}) {expected_dict}"

            self.assertEqual(str(obj), expected_str)
