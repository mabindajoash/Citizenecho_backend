#!/usr/bin/python3


def get_db_storage():
    from models.engine.storage import DBStorage
    return DBStorage()

storage = get_db_storage()
storage.reload()