from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_mail import Mail

from config import Config


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"


from flaskblog.models import User, Post





def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from flaskblog.users.routs import users
    from flaskblog.posts.routs import posts
    from flaskblog.main.routs import main
    from flaskblog.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    @app.shell_context_processor
    def make_shell_context():
        return {"db": db, "User": User, "Post": Post, "current_user": current_user}

    return app
