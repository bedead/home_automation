import os

# these class is imported by __init__.py entry point where all the blueprints are loaded
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = True
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# configuration setting for production server
class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False

# configuration setting for development server
class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True