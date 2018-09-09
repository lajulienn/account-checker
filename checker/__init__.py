import os

from flask import Flask
from flask_pymongo import PyMongo


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        MONGO_DBNAME='checker_db',
        MONGO_URI='mongodb://localhost:27017/checker_db',
    )
    mongo = PyMongo(app)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
