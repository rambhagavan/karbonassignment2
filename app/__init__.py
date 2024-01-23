# app/__init__.py
from flask import Flask

def create_app():
    app = Flask(__name__)

    # Add your configuration, blueprints, and other setup here
    from .views import page1_blueprint
    app.register_blueprint(page1_blueprint, url_prefix='/page1')

    return app

