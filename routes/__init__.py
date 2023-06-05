# entry point for all routes in application
# @author Satyam Mishra

from flask import Flask
from routes.__config__ import DevConfig, ProdConfig

def create_app():
    """Create Flask application."""
    name = "Home Automation"
    app = Flask(name, instance_relative_config=False)
    # selecting config file for application to run
    # Basic config, Dev, and Prod
    app.config.from_object(DevConfig)
    
    with app.app_context():
        # Import parts of our application
        from .__base__ import base_page_bp
        from .__auth__ import auth_page_bp
        from .__error__ import error_page_bp
        from .users.__consumer__ import consumer_page_bp
        from .users.__producer__ import producer_page_bp
        from .users.__aggregator__ import aggregator_page_bp

        # Register Blueprints
        app.register_blueprint(base_page_bp)
        app.register_blueprint(auth_page_bp)
        app.register_blueprint(error_page_bp)
        app.register_blueprint(consumer_page_bp)
        app.register_blueprint(producer_page_bp)
        app.register_blueprint(aggregator_page_bp)

        # returning app
        return app