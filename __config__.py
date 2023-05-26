import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
# these class is imported by __init__.py entry point where all the blueprints are loaded
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = True
    SUPABASE_URL: str = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY: str = os.environ.get("SUPABASE_KEY")
    # print(SUPABASE_URL, SUPABASE_KEY)

    supabase_: Client = create_client(supabase_url=SUPABASE_URL, supabase_key=SUPABASE_KEY)

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