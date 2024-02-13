# https://flask-wtf.readthedocs.io/en/1.0.x/quickstart/
# https://wtforms.readthedocs.io/en/3.0.x/
# https://flask-ckeditor.readthedocs.io/en/latest/basic.html
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


class BlogForm(FlaskForm):
    title = StringField(
        label="Blog Post Title",
        validators=[DataRequired()]
    )
    subtitle = StringField(
        label="Subtitle",
        validators=[DataRequired()]
    )
    author = StringField(
        label="Your Name",
        validators=[DataRequired()]
    )
    img_url = URLField(
        label="Blog Image URL",
        validators=[URL()]
    )
    body = CKEditorField(
        label="Blog Content",
        validators=[DataRequired()]
    )
    submit = SubmitField(
        label="Submit Post"
    )
