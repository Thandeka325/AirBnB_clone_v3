#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import hashlib


class User(BaseModel, Base):
    """Representation of a user"""
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """Initializes user, hashes password if provided"""
        if "password" in kwargs:
            kwargs["password"] = self.hash_password(kwargs["password"])
        super().__init__(*args, **kwargs)

    def hash_password(self, password):
        """Hashes a password using MD5"""
        return hashlib.md5(password.encode()).hexdigest()

    @property
    def password(self):
        """Password getter (disabled for security reasons)"""
        return None

    @password.setter
    def password(self, pwd):
        """Hashes and sets the password"""
        self.__dict__["password"] = self.hash_password(pwd)
