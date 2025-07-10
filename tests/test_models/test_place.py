#!/usr/bin/python3
""" test place model"""


import unittest
from models.place import Place


class TestBaseModel(unittest.TestCase):
    """ Test User class"""
    def test_class_attributes_type(self):
        self.assertIsInstance(Place.city_id, str)
        self.assertIsInstance(Place.user_id, str)
        self.assertIsInstance(Place.name, str)
        self.assertIsInstance(Place.description, str)
        self.assertIsInstance(Place.number_rooms, int)
        self.assertIsInstance(Place.number_bathrooms, int)
        self.assertIsInstance(Place.max_guest, int)
        self.assertIsInstance(Place.price_by_night, int)
        self.assertIsInstance(Place.latitude, float)
        self.assertIsInstance(Place.longitude, float)
        self.assertIsInstance(Place.amenity_ids, list)


    # def test_class_attributes_data(self):
    #     self.assertEqual(Review.place_id, "")
    #     self.assertEqual(Review.user_id, "")
    #     self.assertEqual(Review.text, "")
