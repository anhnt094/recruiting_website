from config import Config
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

Bootstrap(app)


# Khai bao trang login - login() function, se dung url_for() de tim duong dan
login.login_view = 'login'  

from app import routes, models
