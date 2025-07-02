#!/usr/bin/python3
"""
the Base model
"""
import uuid
from datetime import datetime


class BaseModel:
    """
    the base class
    that defines all common attributes/methods
    for other classes:
    """
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __str__(self):
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        self.updated_at = datetime.now()

    def to_dict(self):
        now = datetime.now()
        iso_string = now.isoformat()
        self.__dict__["__class__"] = self.__class__.__name__
        self.__dict__["created_at"] = iso_string
        self.__dict__["updated_at"] = iso_string
        return self.__dict__
