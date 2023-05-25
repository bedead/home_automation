# entry point for all routes in application
# @author Satyam Mishra

from flask import Flask
from config import DevConfig, ProdConfig

def create_app():
    """Create Flask application."""
    name = "Home Automation"
    app = Flask(name, instance_relative_config=False)
    # selecting config file for application to run
    # Basic config, Dev, and Prod
    app.config.from_object(DevConfig)

    with app.app_context():
        # Import parts of our application
        from .base import base_page_bp
        from .auth import auth_page_bp

        # Register Blueprints
        app.register_blueprint(base_page_bp)
        app.register_blueprint(auth_page_bp)

        # returning app
        return app