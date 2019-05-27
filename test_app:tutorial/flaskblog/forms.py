import secrets
import os

from PIL import Image

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from flaskblog.models import User, Post

from flaskblog import app, db


class RegistrationForm(FlaskForm):
    username = StringField(
        label="Username", validators=[DataRequired(), Length(min=2, max=20)]
    )

    email = StringField(label="Email", validators=[DataRequired(), Email()])

    password = PasswordField(label="Password", validators=[DataRequired()])

    confirm_password = PasswordField(
        label="Confirm Password",
        validators=[DataRequired(), EqualTo(fieldname="password")],
    )

    submit = SubmitField(label="Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "This name is alredy taken! Please choose another one."
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "This email is alredy taken! Please choose another one."
            )


class LoginForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    remember = BooleanField(label="Remember Me")
    submit = SubmitField(label="Log In")


class UpdateAccountForm(FlaskForm):
    username = StringField(
        label="Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    picture = FileField(
        label="Update your avatar", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField(label="Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "This name is alredy taken! Please choose another one."
                )

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.get_by_email(email.data)
            if user:
                raise ValidationError(
                    "This name is alredy taken! Please choose another one."
                )

    def load_user(self, user):
        """Loads users username and email into the form
        """
        self.username.data = user.username
        self.email.data = user.email

    def save_picture(self, prev_pic):
        random_hex = secrets.token_hex(8)
        _, file_ext = os.path.splitext(self.picture.data.filename)
        picture_file_n = random_hex + file_ext
        picture_path = os.path.join(
            app.root_path, "static/profile_pics", picture_file_n
        )
        image_size = (125, 125)
        i = Image.open(self.picture.data)
        i.thumbnail(image_size)
        i.save(picture_path)
        if prev_pic != "default.jpg":
            os.remove(os.path.join(app.root_path, "static/profile_pics", prev_pic))

        return picture_file_n


class PostForm(FlaskForm):
    title = StringField(
        label="Title", validators=[DataRequired(), Length(min=3, max=80)]
    )
    content = TextAreaField(label="Content", validators=[DataRequired()])
    submit = SubmitField(label="Post")

    def create_post(self, user):
        post = Post(title=self.title.data, content=self.content.data, author=user)
        db.session.add(post)
        db.session.commit()

        return post

    def load_post(self, post):
        """Loads post title and content into the form
        """
        self.title.data = post.title
        self.content.data = post.content

    def update_post(self, post):
        post.title = self.title.data
        post.content = self.content.data
        db.session.commit()
