import os
from flask import Flask

from checker import checker


# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    MONGO_DBNAME='checker_db',
    MONGO_URI='mongodb://localhost:27017/checker_db',
)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# apply the blueprints to the app
app.register_blueprint(checker.bp)
