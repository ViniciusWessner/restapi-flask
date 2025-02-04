import os
from mongomock import MongoClient



class DevConfig():

    MONGODB_SETTINGS = {
        'db': os.getenv('MONGODB_DB'),
        'host': os.getenv('MONGODB_HOST'),
        'username': os.getenv('MONGODB_USER'),
        'password': os.getenv('MONGODB_PASSWORD'),
    }


class MockConfig():

    MONGODB_SETTINGS = {
        'db': 'users',
        'mongo_client_class': MongoClient
    }
