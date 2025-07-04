#!/usr/bin/python3
""" test file storage module """


import unittest
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from datetime import datetime
import os
import json


class TestFileStorage(unittest.TestCase):
    """
    test FileStorage class
    """
    def test_file_path_attr(self):
        f_storage = FileStorage()
        self.assertEqual(f_storage._FileStorage__file_path, "file.json")

    def setUp(self):
        """Set up test environment"""
        self.storage = FileStorage()
        self.file_path = FileStorage._FileStorage__file_path
        try:
            os.remove(self.file_path)
        except:
            pass
        FileStorage._FileStorage__objects = {}

    def tearDown(self):
        """Clean up after tests"""
        try:
            os.remove(self.file_path)
        except:
            pass

    def test_private_attributes(self):
        """Test private class attributes"""
        self.assertTrue(hasattr(FileStorage, "_FileStorage__file_path"))
        self.assertTrue(hasattr(FileStorage, "_FileStorage__objects"))
        self.assertEqual(type(FileStorage._FileStorage__file_path), str)
        self.assertEqual(type(FileStorage._FileStorage__objects), dict)

    def test_all_method(self):
        """Test all() method"""
        objects = self.storage.all()
        self.assertEqual(type(objects), dict)
        self.assertIs(objects, FileStorage._FileStorage__objects)

    def test_new_method(self):
        """Test new() method"""
        bm = BaseModel()
        self.storage.new(bm)
        key = f"BaseModel.{bm.id}"
        self.assertIn(key, self.storage.all())
        self.assertEqual(self.storage.all()[key], bm)

    def test_save_method(self):
        """Test save() method"""
        bm = BaseModel()
        self.storage.new(bm)
        self.storage.save()
        
        self.assertTrue(os.path.exists(self.file_path))
        
        with open(self.file_path, 'r') as f:
            content = json.load(f)
        
        key = f"BaseModel.{bm.id}"
        self.assertIn(key, content)
        self.assertEqual(content[key]["id"], bm.id)
        self.assertEqual(content[key]["__class__"], "BaseModel")

    def test_reload_method(self):
        """Test reload() method"""
        bm = BaseModel()
        key = f"BaseModel.{bm.id}"
        self.storage.new(bm)
        self.storage.save()
        
        # Clear current objects
        FileStorage._FileStorage__objects = {}
        
        # Reload from file
        self.storage.reload()
        
        objects = self.storage.all()
        self.assertIn(key, objects)
        
        reloaded = objects[key]
        self.assertEqual(reloaded.id, bm.id)
        self.assertEqual(reloaded.created_at, bm.created_at)
        self.assertEqual(reloaded.updated_at, bm.updated_at)
        self.assertEqual(reloaded.__class__.__name__, "BaseModel")

    def test_reload_empty_file(self):
        """Test reload() with empty/non-existent file"""
        try:
            os.remove(self.file_path)
        except:
            pass
        
        # Should not raise any exception
        self.storage.reload()
        self.assertEqual(self.storage.all(), {})

    def test_save_reload_multiple_objects(self):
        """Test saving and reloading multiple objects"""
        objects = []
        for i in range(5):
            bm = BaseModel()
            objects.append(bm)
            self.storage.new(bm)
        
        self.storage.save()
        
        # Clear current objects
        FileStorage._FileStorage__objects = {}
        
        # Reload
        self.storage.reload()
        
        reloaded_objects = self.storage.all()
        self.assertEqual(len(reloaded_objects), 5)
        
        for bm in objects:
            key = f"BaseModel.{bm.id}"
            self.assertIn(key, reloaded_objects)
            reloaded = reloaded_objects[key]
            self.assertEqual(reloaded.id, bm.id)
            self.assertEqual(reloaded.created_at, bm.created_at)

    def test_datetime_conversion(self):
        """Test datetime conversion in save/reload"""
        bm = BaseModel()
        self.storage.new(bm)
        self.storage.save()
        
        # Clear and reload
        FileStorage._FileStorage__objects = {}
        self.storage.reload()
        
        reloaded = self.storage.all()[f"BaseModel.{bm.id}"]
        
        # Check datetime attributes
        self.assertEqual(type(reloaded.created_at), datetime)
        self.assertEqual(type(reloaded.updated_at), datetime)
        self.assertEqual(reloaded.created_at, bm.created_at)
        self.assertEqual(reloaded.updated_at, bm.updated_at)

    def test_new_with_invalid_object(self):
        """Test new() with invalid object"""
        with self.assertRaises(AttributeError):
            self.storage.new("not an object")
        with self.assertRaises(AttributeError):
            self.storage.new(None)
        with self.assertRaises(AttributeError):
            self.storage.new(123)