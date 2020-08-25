from flask import Flask
from application.utilities.flask import APIError, APIFlask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from application.configs import Config
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = APIFlask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    db.init_app(app)
    Migrate(app, db)
    CORS(app)
    with app.app_context():
        from application.routes.web_api.api import dash_bp
        app.register_blueprint(dash_bp, url_prefix="")
    return app

    
