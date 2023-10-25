from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.api.routes import api

from models import loginManager, db
from app.site.routes import site
from app.authentication.routes import auth  
app = Flask(__name__) 
app.register_blueprint(auth)
app.register_blueprint(site)
app.register_blueprint(api)
app.config.from_object(Config)
#db = SQLAlchemy(app)
migrate = Migrate(app, db)
#loginManager = LoginManager(app)
db.init_app(app)
loginManager.init_app(app)




