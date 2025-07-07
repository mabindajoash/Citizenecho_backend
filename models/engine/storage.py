#!/usr/bin/python3

from models.base_model import BaseModel
from models.base_model import Base
from models.users import User
from models.inquiries import Inquiry
from models.reports import Report
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        user = getenv('USER', 'root')
        passwd = getenv('PASSWORD', '')
        host = getenv('HOST', 'localhost')
        db = getenv('DB', 'citizenecho_db')
        port = getenv('PORT', '3306')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:{}/{}'.format(
            user, passwd, host, port, db))

    def all(self, cls=None):
        """retrieve all objects of a class"""
        objects = {}
        if cls:
            query = self.__session.query(cls).all()
            for obj in query:
                key = f"{type(obj).__name__}.{obj.id}"
                objects[key] = obj.to_dict()
        else:
            for class_ in [Inquiry, Report, User]:
                query = self.__session.query(class_).all()
                for obj in query:
                    key = f"{type(obj).__name__}.{obj.id}"
                    objects[key] = obj.to_dict()
        return objects

    def get_by(self, cls, **kwargs):
        return self.__session.query(cls).filter_by(**kwargs).first()

    def get_all_by(self, cls, **kwargs):
        return self.__session.query(cls).filter_by(**kwargs).all()

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj is not None:
            self.__session.delete(obj)

    def rollback(self):
        self.__session.rollback()

    def reload(self):
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()

    def close(self):
        self.__session.close()