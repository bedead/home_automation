from routes import create_app
# from pyneutralino import PyNeutralino
# this is main wsgi runner file which imports the required configuration 
# setting from __init__.py file and creates an app
if __name__=="__main__":
    app = create_app()
    app.run()