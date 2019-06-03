import os
import secrets

from PIL import Image

from flask import current_app
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_wtf.file import FileField, FileAllowed
from flaskblog.models import User


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

    def save_picture(self):
        random_hex = secrets.token_hex(8)
        _, file_ext = os.path.splitext(self.picture.data.filename)
        picture_file_n = random_hex + file_ext
        picture_path = os.path.join(
            current_app.root_path, "static/profile_pics", picture_file_n
        )
        image_size = (125, 125)
        i = Image.open(self.picture.data)
        i.thumbnail(image_size)
        i.save(picture_path)
        exist_pics = os.listdir(os.path.join(current_app.root_path, 'static/profile_pics'))
        if current_user.image_file in exist_pics and current_user.image_file != "default.jpg":
            os.remove(os.path.join(current_app.root_path, "static/profile_pics", current_user.image_file))

        return picture_file_n


class RequestResetForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email!')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label='Reset Password')
