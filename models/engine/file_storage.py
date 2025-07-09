#!/usr/bin/python3
"""
the File Storage model
"""
import json
from datetime import datetime


class FileStorage:
    """
    save to and reload data from json files
    """
    __objects = {}
    __file_path = "file.json"

    
    def all(self):
        """
        return all objects of the class
        """
        return FileStorage.__objects
        # OR for more flexability if needed later
        # return self.__class__.__objects
    
    def new(self, obj):
        """
        add new object with unique id
        """
        from ..base_model import BaseModel  # Lazy import
        from ..user import User

        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """
        serielize objects and add them to Json file
        """
        with open(FileStorage.__file_path, 'w') as file:
            json.dump({key: value.to_dict() for key, value in FileStorage.__objects.items()}, file)

    def reload(self):
        """
        deserielze  object back to objects
        """
        try:
            with open(FileStorage.__file_path, 'r') as file:
                from ..base_model import BaseModel  # Lazy import
                from ..user import User

                objects = json.load(file)
                for key, value in objects.items():
                    class_name = value["__class__"]
                    value["created_at"] = datetime.strptime(value["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
                    value["updated_at"] = datetime.strptime(value["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
                    FileStorage.__objects[key] = eval(class_name)(**value)

        except FileNotFoundError:
            pass