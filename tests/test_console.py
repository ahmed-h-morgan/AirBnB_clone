#!/usr/bin/python3
"""Unit tests for console.py"""
import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.user import User
import os


class TestConsole(unittest.TestCase):
    """Test cases for the HBNB console"""

    def setUp(self):
        """Set up test environment"""
        self.console = HBNBCommand()
        if os.path.exists("file.json"):
            os.remove("file.json")

    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_quit(self):
        """Test quit command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.console.onecmd("quit"))

    def test_EOF(self):
        """Test EOF command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.console.onecmd("EOF"))

    def test_emptyline(self):
        """Test empty line input"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("")
            self.assertEqual(f.getvalue(), "")

    def test_create_missing_class(self):
        """Test create with missing class"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create")
            self.assertEqual(f.getvalue().strip(), "** class name missing **")

    def test_create_invalid_class(self):
        """Test create with invalid class"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create MyModel")
            self.assertEqual(f.getvalue().strip(), "** class doesn't exist **")

    def test_create_valid_class(self):
        """Test create with valid class"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create BaseModel")
            output = f.getvalue().strip()
            self.assertTrue(len(output) == 36)  # UUID length

    def test_show_missing_class(self):
        """Test show with missing class"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show")
            self.assertEqual(f.getvalue().strip(), "** class name missing **")

    def test_show_invalid_class(self):
        """Test show with invalid class"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show MyModel")
            self.assertEqual(f.getvalue().strip(), "** class doesn't exist **")

    def test_show_missing_id(self):
        """Test show with missing id"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show BaseModel")
            self.assertEqual(f.getvalue().strip(), "** instance id missing **")

    def test_show_no_instance(self):
        """Test show with non-existent instance"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show BaseModel 12345")
            self.assertEqual(f.getvalue().strip(), "** no instance found **")

    def test_destroy_missing_class(self):
        """Test destroy with missing class"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy")
            self.assertEqual(f.getvalue().strip(), "** class name missing **")

    def test_destroy_invalid_class(self):
        """Test destroy with invalid class"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy MyModel")
            self.assertEqual(f.getvalue().strip(), "** class doesn't exist **")

    def test_destroy_missing_id(self):
        """Test destroy with missing id"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy BaseModel")
            self.assertEqual(f.getvalue().strip(), "** instance id missing **")

    def test_destroy_no_instance(self):
        """Test destroy with non-existent instance"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy BaseModel 12345")
            self.assertEqual(f.getvalue().strip(), "** no instance found **")

    def test_all_no_class(self):
        """Test all with no class specified"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("all")
            self.assertTrue(isinstance(eval(f.getvalue()), list))

    def test_all_invalid_class(self):
        """Test all with invalid class"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("all MyModel")
            self.assertEqual(f.getvalue().strip(), "** class doesn't exist **")

    def test_update_missing_class(self):
        """Test update with missing class"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update")
            self.assertEqual(f.getvalue().strip(), "** class name missing **")

    def test_update_invalid_class(self):
        """Test update with invalid class"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update MyModel")
            self.assertEqual(f.getvalue().strip(), "** class doesn't exist **")

    def test_update_missing_id(self):
        """Test update with missing id"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update BaseModel")
            self.assertEqual(f.getvalue().strip(), "** instance id missing **")

    def test_update_no_instance(self):
        """Test update with non-existent instance"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update BaseModel 12345")
            self.assertEqual(f.getvalue().strip(), "** no instance found **")

    def test_update_missing_attr(self):
        """Test update with missing attribute"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create BaseModel")
            obj_id = f.getvalue().strip()
            cmd = f"update BaseModel {obj_id}"
            with patch('sys.stdout', new=StringIO()) as f2:
                self.console.onecmd(cmd)
                self.assertEqual(f2.getvalue().strip(), "** attribute name missing **")

    def test_update_missing_value(self):
        """Test update with missing value"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create BaseModel")
            obj_id = f.getvalue().strip()
            cmd = f"update BaseModel {obj_id} first_name"
            with patch('sys.stdout', new=StringIO()) as f2:
                self.console.onecmd(cmd)
                self.assertEqual(f2.getvalue().strip(), "** value missing **")

    def test_class_all(self):
        """Test <class name>.all() syntax"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("BaseModel.all()")
            self.assertTrue(isinstance(eval(f.getvalue()), list))

    def test_class_count(self):
        """Test <class name>.count() syntax"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("BaseModel.count()")
            count = int(f.getvalue().strip())
            self.assertGreaterEqual(count, 0)

    def test_class_show(self):
        """Test <class name>.show(<id>) syntax"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create BaseModel")
            obj_id = f.getvalue().strip()
            cmd = f"BaseModel.show({obj_id})"
            with patch('sys.stdout', new=StringIO()) as f2:
                self.console.onecmd(cmd)
                output = f2.getvalue().strip()
                self.assertIn(obj_id, output)

    def test_class_destroy(self):
        """Test <class name>.destroy(<id>) syntax"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create BaseModel")
            obj_id = f.getvalue().strip()
            cmd = f"BaseModel.destroy({obj_id})"
            with patch('sys.stdout', new=StringIO()) as f2:
                self.console.onecmd(cmd)
                self.assertEqual(f2.getvalue().strip(), "")
            # Verify object was actually destroyed
            with patch('sys.stdout', new=StringIO()) as f3:
                self.console.onecmd(f"show BaseModel {obj_id}")
                self.assertEqual(f3.getvalue().strip(), "** no instance found **")

    def test_class_update(self):
        """Test <class name>.update(<id>, <attr>, <value>) syntax"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create BaseModel")
            obj_id = f.getvalue().strip()
            cmd = f'BaseModel.update("{obj_id}", "name", "test_value")'
            with patch('sys.stdout', new=StringIO()) as f2:
                self.console.onecmd(cmd)
                self.assertEqual(f2.getvalue().strip(), "")
            # Verify update worked
            with patch('sys.stdout', new=StringIO()) as f3:
                self.console.onecmd(f'show BaseModel {obj_id}')
                output = f3.getvalue().strip()
                self.assertIn("'name': 'test_value'", output)

    def test_class_update_dict(self):
        """Test <class name>.update(<id>, <dictionary>) syntax"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create BaseModel")
            obj_id = f.getvalue().strip()
            cmd = f'BaseModel.update("{obj_id}", {{"name": "test", "number": 89}})'
            with patch('sys.stdout', new=StringIO()) as f2:
                self.console.onecmd(cmd)
                self.assertEqual(f2.getvalue().strip(), "")
            # Verify update worked
            with patch('sys.stdout', new=StringIO()) as f3:
                self.console.onecmd(f'show BaseModel {obj_id}')
                output = f3.getvalue().strip()
                self.assertIn("'name': 'test'", output)
                self.assertIn("'number': 89", output)


if __name__ == '__main__':
    unittest.main()