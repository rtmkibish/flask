from datetime import datetime

from flask import current_app
from flaskblog import db, login_manager

from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True, cascade='all,delete')
    comments = db.relationship('PostComment', backref='author', lazy=True, cascade='all,delete')

    @classmethod
    def create_user(cls, form, u_password):
        user = cls(username=form.username.data, email=form.email.data, password=u_password)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        token = s.dumps({'user_id': self.id}).decode('utf-8')
        return token

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None

        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    comments = db.relationship('PostComment', backref='post', lazy=True, cascade='all,delete')

    def __repr__(self):
        return f"Post('{self.title}', {self.date_posted})"

    def post_delete(self):
        db.session.delete(self)
        db.session.commit()


class PostComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('post_comment.id'), nullable=True)
    parents = db.relationship('PostComment', backref=db.backref('parent', remote_side='PostComment.id'), lazy=True)

    def __repr__(self):
        return f"PostComment('{self.id}', '{self.comment_text[:10]}' {self.parent_id})"

    @classmethod
    def create_comment(cls, form, post, author):
        comment = cls(comment_text=form.text_comment.data, post_id=post.id, user_id=author.id)
        db.session.add(comment)
        db.session.commit()
        return comment

    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def add_reply(cls, form, post_id, author_id, parent_id):
        reply = cls(comment_text=form.text_comment.data, post_id=post_id, user_id=author_id, parent_id=parent_id)
        db.session.add(reply)
        db.session.commit()

