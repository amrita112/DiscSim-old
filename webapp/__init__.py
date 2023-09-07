from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

webapp = Flask(__name__)
webapp.config.from_object(Config)
db = SQLAlchemy(webapp)
migrate = Migrate(webapp, db)


from webapp import routes, models # This statement is at the end of this file because routes will import app, so this avoids an error 
                                  # due to mutual referencing between these files. 