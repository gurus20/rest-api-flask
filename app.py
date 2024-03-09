import os
from flask import Flask
from configparser import ConfigParser
from flask_migrate import Migrate
from db.init_db import db
from routes.auth_routes import bp as routes_bp
from helpers.common import cache
from flask_mail import Mail

def create_app():
    app = Flask(__name__)

    # Load configuration
    load_config(app)

    # Initialize Database
    db.init_app(app)

    # Setup migrate
    migrate = Migrate(app, db)

    # mail setup
    mail = Mail(app)

    # cache setup
    cache.init_app(app)

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

    # Configure Flask-Mail
    app.config['MAIL_SERVER'] = config[config_type]['MAIL_SERVER']
    app.config['MAIL_PORT'] = config[config_type]['MAIL_PORT']
    app.config['MAIL_USE_TLS'] = config[config_type]['MAIL_USE_TLS']
    app.config['MAIL_USERNAME'] = config[config_type]['MAIL_USERNAME']
    app.config['MAIL_PASSWORD'] = config[config_type]['MAIL_PASSWORD']

if __name__ == "__main__":
    # Load configuration
    app = create_app()

    # Start application to serve 
    app.run()
