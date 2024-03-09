import os
from flask import Flask
from configparser import ConfigParser
from flask_migrate import Migrate
from db.init_db import db
from routes.auth_routes import bp as routes_bp

def create_app():
    app = Flask(__name__)

    # Load configuration
    load_config(app)

    # Initialize Database
    db.init_app(app)

    # Setup migrate
    migrate = Migrate(app, db)

    # Register the Blueprint
    app.register_blueprint(routes_bp)

    return app

def load_config(app):
    config = ConfigParser()
    config.read('config.ini')

    # Set environment explicitly or use a default value
    environment = os.environ.get('FLASK_ENV', 'development')

    if environment == 'development':
        config_type = 'development'
    else:
        config_type = 'production'

    app.config['SECRET_KEY'] = config[config_type]['SECRET_KEY']
    app.config['SQLALCHEMY_DATABASE_URI'] = config[config_type]['SQLALCHEMY_DATABASE_URI']
    app.config['DEBUG'] = config[config_type].getboolean('DEBUG')

if __name__ == "__main__":
    # Load configuration
    app = create_app()

    # Start application to serve
    app.run()
