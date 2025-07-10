#!/usr/bin/python3
""" test review model"""


import unittest
from models.review import Review


class TestBaseModel(unittest.TestCase):
    """ Test User class"""
    def test_class_attributes_type(self):
        self.assertIsInstance(Review.place_id, str)
        self.assertIsInstance(Review.user_id, str)
        self.assertIsInstance(Review.text, str)

    def test_class_attributes_data(self):
        self.assertEqual(Review.place_id, "")
        self.assertEqual(Review.user_id, "")
        self.assertEqual(Review.text, "")
