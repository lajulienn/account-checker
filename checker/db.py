from flask import current_app, g
from flask_pymongo import PyMongo


def get_db():
    """
    Get the application's configured database.
    """
    if 'db' not in g:
        g.db = PyMongo(current_app)
    return g.db
