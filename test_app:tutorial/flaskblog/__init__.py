from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_mail import Mail

from config import Config

# from forms import RegistrationForm, LoginForm


app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from flaskblog import routs, models
from flaskblog.models import User, Post


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Post": Post, "current_user": current_user}
