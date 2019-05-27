import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "f90be35e025e0af98d9a25bb2f8295b4"
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("SQLALCHEMY_DATABASE_URI")
        or f"sqlite:///{os.path.join(basedir, 'site.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
