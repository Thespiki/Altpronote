from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_object=None):
    app = Flask(__name__)
    app.config.setdefault('SQLALCHEMY_DATABASE_URI', 'sqlite:///altpronote.db')
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)

    db.init_app(app)

    # Register blueprints / routes
    from .auth import auth_bp
    app.register_blueprint(auth_bp)
    from .frontend import frontend_bp
    app.register_blueprint(frontend_bp)

    return app
