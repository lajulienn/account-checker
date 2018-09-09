import os

from flask import Flask
from flask import jsonify
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

    def has_account(phone_or_email):
        pass

    @app.route('/check_user/<phone_or_email>', methods=['POST'])
    def check_user(phone_or_email):
        users_db = mongo.db.users

        # Check if user info is already id DB
        user_entry = users_db.find_one({'login': phone_or_email})
        if user_entry:
            # Return result from DB
            output = {'Account exist': True}
        else:
            # Send request and write to DB
            output = {'Account exist': False}
            phone_id = users_db.insert({'phone': phone, 'Account exist': True})

        return jsonify({'result': output})

    return app
