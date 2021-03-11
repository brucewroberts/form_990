import os

from flask import Flask, g, request
from flask_cors import CORS

from app.blueprint_main.routes import main
from app.blueprint_api.routes import api
import app.lib.config as config
import app.lib.db as db


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(api, url_prefix='/api/v1')

    # Run the initializaton for some modules
    with app.app_context():
        config.init()

    # Must be after config.init() since that loads the secret.
    app.config['SECRET_KEY'] = config.get_secret_key()

    return app
