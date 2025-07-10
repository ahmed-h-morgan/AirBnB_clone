#!/usr/bin/python3
""" test amenity model"""


import unittest
from models.amenity import Amenity


class TestBaseModel(unittest.TestCase):
    """ Test User class"""
    def test_class_attributes_type(self):
        self.assertIsInstance(Amenity.name, str)


    def test_class_attributes_data(self):
        self.assertEqual(Amenity.name, "")
 
