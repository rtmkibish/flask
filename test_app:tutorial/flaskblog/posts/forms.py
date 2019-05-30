from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

from flaskblog.models import Post
from flaskblog import db


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
