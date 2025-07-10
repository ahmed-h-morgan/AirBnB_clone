#!/usr/bin/python3
""" test state model"""


import unittest
from models.state import State


class TestBaseModel(unittest.TestCase):
    """ Test User class"""
    def test_class_attributes_type(self):
        self.assertIsInstance(State.name, str)


    def test_class_attributes_data(self):
        self.assertEqual(State.name, "")
 
