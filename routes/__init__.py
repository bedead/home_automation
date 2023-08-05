# entry point for all routes in application
# @author Satyam Mishra

"""
This code serves as the starting point for building a Flask-based 
application for home automation. It encapsulates the configuration and 
setup of the application, focusing on creating a modular structure through the use 
of blueprints. Let's break down the key components:
The code begins by importing necessary modules, including sentry_sdk for 
performance and error monitoring, as well as Flask to create the application. It also imports configuration 
classes, DevConfig and ProdConfig, from the routes.__config__ module.
The heart of the application is the create_app() function, 
which initializes the Flask app. It sets the application 
name as "Home Automation" and configures it using the DevConfig configuration.
"""

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from flask import Flask
from routes.__config__ import DevConfig, ProdConfig


def create_app():
    """
    Within the context of the app, various blueprints are registered, each
    encapsulating specific parts of the application's functionality:


    base_page_bp: Base routes for the application.
    auth_page_bp: Routes related to authentication.
    error_page_bp: Routes handling error scenarios.
    api_page_bp: Routes related to API interactions.
    api_fetch_bp: Routes for fetching data from APIs.
    api_insert_bp: Routes for inserting data into APIs.
    Blueprints for user roles:
    consumer_page_bp: Routes specific to consumers.
    producer_page_bp: Routes specific to producers.
    utility_page_bp: Routes for utility functions.
    aggregator_page_bp: Routes for aggregator-related tasks.
    """
    name = "Home Automation"
    # performance and error monitoring
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
