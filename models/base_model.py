#!/usr/bin/python3

from datetime import datetime
from sqlalchemy.orm import relationship, declarative_base
import models
from sqlalchemy import DateTime, Column, String
import uuid
import json

Base = declarative_base()

class BaseModel:
    id = Column(String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)
                models.storage.new(self)

        else:
            models.storage.new(self)

    def __str__(self):
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        models.storage.save()

    def to_dict(self):
        """convert to dictionary"""
        """Converts object to dictionary."""
        dict_copy = self.__dict__.copy()
        dict_copy.pop('_sa_instance_state', None)
        dict_copy['id'] = str(self.id)
        dict_copy['created_at'] = self.created_at.isoformat() if self.created_at else None
        dict_copy['updated_at'] = self.updated_at.isoformat() if self.updated_at else None
        return dict_copy


    def to_json(self):
        """convert to json"""
        return json.dumps(self.to_dict())

    def delete(self):
        """delete object"""
        models.storage.delete()