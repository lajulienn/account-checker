from flask import current_app, g
from flask_pymongo import PyMongo


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if 'db' not in g:
        g.db = PyMongo(current_app)
    return g.db

