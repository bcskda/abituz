from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	migrate.init_app(app, db)

	from app.errors import bp as errors_bp
	app.register_blueprint(errors_bp)

	from app.api import bp as api_bp
	app.register_blueprint(api_bp, url_prefix='/api')

	from app.main import bp as main_bp
	app.register_blueprint(main_bp)

	return app

from app import models