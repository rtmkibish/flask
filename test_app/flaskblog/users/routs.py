import os

from flask import Blueprint, render_template, redirect, flash, request, url_for, current_app
from flask_login import current_user, login_user, logout_user, login_required
from flaskblog import bcrypt, db
from flaskblog.users.utils import send_reset_email
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm

from flaskblog.models import User, Post

users = Blueprint('users', __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect("home")

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pasword = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User.create_user(form, hashed_pasword)

        flash("Your account has been created! You are now able to log in", "success")
        return redirect("login")
    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))

        flash("Login unsuccessful. Please check your email and password", "danger")
    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("users.login"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = form.save_picture()
            current_user.image_file = picture_file or current_user.image_file
            flash("The profile image wasn't updated due to invalid file", "danger")
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.load_user(current_user)
    is_image_exist = current_user.image_file in os.listdir(os.path.join(current_app.root_path, 'static/profile_pics'))
    if is_image_exist:
        image_file = url_for("static", filename=f"profile_pics/{current_user.image_file}")
    else:
        image_file = url_for("static", filename=f"profile_pics/default.jpg")
    return render_template(
        "account.html", title="Account", image_file=image_file, form=form
    )


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    exist_files = os.listdir(os.path.join(current_app.root_path + '/static/profile_pics'))
    posts = (
        Post.query.filter_by(author=user)
        .order_by(Post.date_posted.desc())
        .paginate(page=page, per_page=20)
    )
    return render_template("user_posts.html", posts=posts, user=user, exist_files=exist_files)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password!', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password' , form=form)


@users.route('/reset_password/<string:token>', methods=['GET', "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)
    if user is None:
        flash('That is invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
