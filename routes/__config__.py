import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

"""
The Config class acts as the base configuration for the application. It 
retrieves environment variables for the Secret Key, Supabase URL, and 
Supabase Key. Additionally, it creates a supabase_ attribute of the Client 
type using the create_client() function. This attribute allows the 
application to interact with the Supabase database.
The ProdConfig and DevConfig classes extend the Config class and adjust the 
settings based on the environment. In the ProdConfig class, the 
DEBUG attribute is set to False, indicating that debugging 
information should not be displayed. This is suitable for a 
production environment where security and performance are paramount. 
On the other hand, the DevConfig class is tailored for development purposes. 
Both DEBUG and TESTING attributes are set to True, which enables debugging 
information and testing features during development.
"""


# these class is imported by __init__.py entry point where all the blueprints are loaded
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = True
    SUPABASE_URL: str = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY: str = os.environ.get("SUPABASE_KEY")
    # print(SUPABASE_URL, SUPABASE_KEY)

    supabase_: Client = create_client(
        supabase_url=SUPABASE_URL, supabase_key=SUPABASE_KEY
    )


# configuration setting for production server
class ProdConfig(Config):
    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False


# configuration setting for development server
class DevConfig(Config):
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
