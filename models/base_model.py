#!/usr/bin/python3
"""
the Base model
"""
import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """
    the base class
    that defines all common attributes/methods
    for other classes:
    """
    def __init__(self, *args, **kwargs):
        if len(kwargs) == 0:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)
        else:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                elif key in ("created_at", "updated_at"):
                    setattr(self, key, datetime.fromisoformat(value))
                else:
                    setattr(self, key, value)

    def __str__(self):
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        storage.save()
        self.updated_at = datetime.now()

    def to_dict(self):
        # self.__dict__["__class__"] = self.__class__.__name__
        # self.__dict__["created_at"] = self.created_at.isoformat()
        # self.__dict__["updated_at"] = self.updated_at.isoformat()
        # return self.__dict__

        new_dict = self.__dict__.copy()
        new_dict["__class__"] = self.__class__.__name__
        
        # Handle created_at
        if isinstance(self.created_at, datetime):
            new_dict["created_at"] = self.created_at.isoformat()
        else:
            new_dict["created_at"] = self.created_at  # Already a string
        
        # Handle updated_at
        if isinstance(self.updated_at, datetime):
            new_dict["updated_at"] = self.updated_at.isoformat()
        else:
            new_dict["updated_at"] = self.updated_at  # Already a string
        
        return new_dict