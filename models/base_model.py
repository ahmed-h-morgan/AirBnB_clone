#!/usr/bin/python3
"""
the Base model for all inhereted models
contain all common attributes and methods between all models
"""
import uuid
from datetime import datetime

class BaseModel:
    """the main / parent class"""
    def __init__(self) -> None:
        # assign id when instance created
        self.id = str(uuid.uuid4())

        # assign with the current datetime when an instance is created
        self.created_at = datetime.now()

        # assign with the current datetime when an instance is created
        # and it will be updated every time you change your object
        self.updated_at = datetime.now()

    # The __str__() method returns a human-readable string representation\
    # of an object
    def __str__(self) -> str:
        return f'[{self.__class__.__name__}] ({self.id}) {self.__dict__}'
    
    # updates the public instance attribute updated_at with the current datetime
    def save(self):
        self.updated_at = datetime.now()

    
    def to_dict(self):
        self.created_at = datetime.isoformat(self.created_at)
        self.updated_at = datetime.isoformat(self.updated_at)
        self.__dict__.__setitem__('__class__', self.__class__.__name__)
    
