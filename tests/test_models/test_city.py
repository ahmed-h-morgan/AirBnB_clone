#!/usr/bin/python3
""" test city model"""


import unittest
from models.city import City


class TestBaseModel(unittest.TestCase):
    """ Test User class"""
    def test_class_attributes_type(self):
        self.assertIsInstance(City.name, str)
        self.assertIsInstance(City.state_id, str)

    def test_class_attributes_data(self):
        self.assertEqual(City.name, "")
        self.assertEqual(City.state_id, "")
 
