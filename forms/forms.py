# https://flask-wtf.readthedocs.io/en/1.0.x/quickstart/
# https://wtforms.readthedocs.io/en/3.0.x/
# https://flask-ckeditor.readthedocs.io/en/latest/basic.html
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, EmailField, PasswordField
from wtforms.validators import DataRequired, URL, Length, Email
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
    # Likely no longer needed as the author is now a User object.
    # author = StringField(
    #     label="Your Name",
    #     validators=[DataRequired()]
    # )
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


class RegisterForm(FlaskForm):
    email = EmailField(
        label="Email",
        validators=[Email(), DataRequired()]
    )
    password = PasswordField(
        label="Password",
        validators=[Length(min=8), DataRequired()]
    )
    name = StringField(
        label="Name",
        validators=[DataRequired()]
    )
    submit = SubmitField(
        label="Sign me up!"
    )


class LoginForm(FlaskForm):
    email = EmailField(
        label="Email",
        validators=[Email(), DataRequired()]
    )
    password = PasswordField(
        label="Password",
        validators=[Length(min=8), DataRequired()]
    )
    submit = SubmitField(
        label="Let me in!"
    )


class CommentForm(FlaskForm):
    comment = CKEditorField(
        label="Comment",
        validators=[DataRequired()]
    )
    submit = SubmitField(
        label="Submit Comment"
    )
