import os

from flask import Blueprint, render_template, redirect, flash, abort, request, url_for, current_app
from flask_login import login_required, current_user

from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        form.create_post(current_user)
        flash("The post has been created!", "success")
        return redirect(url_for("main.home"))
    return render_template(
        "create_post.html", title="New Post", form=form, legend="New Post"
    )


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    is_img_exist = post.author.image_file in os.listdir(os.path.join(current_app.root_path + '/static/profile_pics'))
    return render_template("post.html", post=post, is_img_exist=is_img_exist)


@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        form.update_post(post)
        flash("Your post has been updated!", "success")
        return redirect(url_for("posts.post", post_id=post.id))
    elif request.method == "GET":
        form.load_post(post)
    return render_template(
        "create_post.html", title="Update Post", form=form, legend="Post Update"
    )


@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    post.post_delete()
    flash("The post has been deleted successfuly!", "success")
    return redirect(url_for("main.home"))