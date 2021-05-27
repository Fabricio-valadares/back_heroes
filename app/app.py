from flask import Flask
from app import views
from app.configurations import database
from app.configurations import migrations
from app import configurations
from app.configurations import jwt_authentication
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    configurations.init_app(app)
    
    database.init_app(app)
    migrations.init_app(app)
    views.init_app(app)
    jwt_authentication.init_app(app)

    return app
