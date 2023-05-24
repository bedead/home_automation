import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = True
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True