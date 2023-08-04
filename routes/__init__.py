# entry point for all routes in application
# @author Satyam Mishra

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from flask import Flask
from routes.__config__ import DevConfig, ProdConfig


def create_app():
    """Create Flask application."""
    name = "Home Automation"
    # performance and error monitoring
    sentry_sdk.init(
        dsn="https://97c12bf6390dfb2ef1a42990a32e3813@o4505618450743296.ingest.sentry.io/4505618452905984",
        integrations=[
            FlaskIntegration(),
        ],
        traces_sample_rate=1.0,
    )
    app = Flask(name, instance_relative_config=False)
    # selecting config file for application to run
    # Basic config, Dev, and Prod
    app.config.from_object(DevConfig)

    with app.app_context():
        # Import parts of our application
        from .__base__ import base_page_bp
        from .__auth__ import auth_page_bp
        from .__error__ import error_page_bp
        from .__api__ import api_page_bp
        from .__apifetch__ import api_fetch_bp
        from .__apiinsert__ import api_insert_bp
        from .users.__consumer__ import consumer_page_bp
        from .users.__producer__ import producer_page_bp
        from .users.__aggregator__ import aggregator_page_bp
        from .users.__utility__ import utility_page_bp

        # Register Blueprints
        app.register_blueprint(base_page_bp)
        app.register_blueprint(auth_page_bp)
        app.register_blueprint(error_page_bp)
        app.register_blueprint(api_page_bp)
        app.register_blueprint(api_fetch_bp)
        app.register_blueprint(api_insert_bp)
        app.register_blueprint(consumer_page_bp)
        app.register_blueprint(producer_page_bp)
        # app.register_blueprint(prosumer_page_bp)
        app.register_blueprint(utility_page_bp)
        app.register_blueprint(aggregator_page_bp)

        # returning app
        return app
