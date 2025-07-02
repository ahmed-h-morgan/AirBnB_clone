#!/usr/bin/python3
"""
the Base model
"""
import uuid


class BaseModel:
    """
    the base class
    that defines all common attributes/methods
    for other classes:
    """
    def __init__(self):
        self.id = str(uuid.uuid4())
        

