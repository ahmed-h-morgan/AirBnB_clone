#!/usr/bin/python3
"""
the All models Package
"""

# from engine.file_storage import FileStorage
from models.engine.file_storage import FileStorage

# FileStorage = __import__('file_storage').FileStorage

storage = FileStorage()

storage.reload