from flask import Flask
import os



def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='4385JH4582IHR-4823808495283450894RW0',
        DATABASE= os.path.join(app.instance_path, 'xallery.sqlite')
    )
    
    if test_config == None:
        
        app.config.from_pyfile('config.py', silent=True)
    else:
        
        app.config.from_mapping(test_config)
        
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    
    
    from . import db
    db.init_app(app)
    
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    
    
    
    return app