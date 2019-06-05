import os
from flask import Blueprint, render_template, request, current_app
from flaskblog.models import Post

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
# @login_required
def home():
    exist_pics = os.listdir(os.path.join(current_app.root_path, 'static/profile_pics'))
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=20, page=page)
    return render_template("home.html", posts=posts, exist_pics=exist_pics)


@main.route("/about")
def about():
    return render_template("about.html", title="About")