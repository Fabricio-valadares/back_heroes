from flask import Flask
from config import selector_config
from os import getenv

def init_app(app: Flask):
    config_type = getenv("FLASK_ENV")
    object_config = selector_config[config_type]
    app.config.from_object(object_config)
