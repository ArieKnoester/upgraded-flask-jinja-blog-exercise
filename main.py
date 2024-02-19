# Templates used: https://startbootstrap.com/previews/clean-blog
# Other template sites. Not used here, but links added for reference:
# https://bootstrapmade.com/
# https://getbootstrap.com/docs/5.0/examples/
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap5
from flask_login import login_user, LoginManager, login_required, logout_user
from flask_gravatar import Gravatar
from werkzeug.security import generate_password_hash, check_password_hash
from models.db import db
from models.blogpost import BlogPost
from models.user import User
from forms.forms import BlogForm, RegisterForm, LoginForm
from flask_ckeditor import CKEditor
import nh3
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv(".env")
HOST_EMAIL = os.environ["HOST_EMAIL"]
FROM_ADDR = os.environ["FROM_ADDR"]
FROM_ADDR_APP_PASSWORD = os.environ["FROM_ADDR_APP_PASSWORD"]
TO_ADDR = os.environ["TO_ADDR"]
SECRET_KEY = os.environ["SECRET_KEY"]

# For the footer's copyright year.
current_year = datetime.datetime.now().year

app = Flask(__name__)
Bootstrap5(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.secret_key = SECRET_KEY
db.init_app(app)
CKEditor(app)
CSRFProtect(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    all_posts = db.session.execute(db.select(BlogPost)).scalars()
    return render_template("index.html", posts=all_posts, year=current_year)


@app.route('/register', methods=["GET", "POST"])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        user_email = register_form.email.data
        user_password = register_form.password.data
        user_name = register_form.name.data

        # Check if email already exists.
        user_exists = db.session.query(db.exists().where(User.email == user_email)).scalar()
        if user_exists:
            flash("An account already exists with that email address. Log in instead.")
            return redirect(url_for('login'))

        hashed_password = generate_password_hash(
            password=user_password,
            method="pbkdf2",
            salt_length=8
        )

        # Pycharm Community Edition apparently has a bug which may highlight
        # these arguments as 'unexpected arguments' when using flask_sqlalchemy
        # and any Mixin class.
        new_user = User(
            email=user_email,
            password=hashed_password,
            name=user_name
        )

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("register.html", form=register_form)


@app.route('/login')
def login():
    login_form = LoginForm()
    return render_template("login.html", form=login_form)


@app.route('/logout')
def logout():
    return redirect(url_for('home'))


@app.route("/post/<int:post_id>")
def display_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    return render_template("post.html", post=post, year=current_year)


@app.route("/new-post", methods=["GET", "POST"])
def new_post():
    new_blog_form = BlogForm()
    if new_blog_form.validate_on_submit():
        new_blog_post = BlogPost(
            title=request.form.get("title"),
            subtitle=request.form.get("subtitle"),
            date=datetime.datetime.now().strftime("%B %d, %Y"),
            body=nh3.clean(request.form.get("body")),
            author=request.form.get("author"),
            img_url=request.form.get("img_url")
        )
        db.session.add(new_blog_post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("make-post.html", form=new_blog_form, h1_text="New Post", year=current_year)


@app.route("/edit-post", methods=["GET", "POST"])
def edit_post():
    post_id = request.args.get("post_id")
    post = db.get_or_404(BlogPost, post_id)
    edit_blog_form = BlogForm(
        title=post.title,
        subtitle=post.subtitle,
        author=post.author,
        img_url=post.img_url,
        body=post.body
    )

    if edit_blog_form.validate_on_submit():
        post.title = edit_blog_form.title.data
        post.subtitle = edit_blog_form.subtitle.data
        post.author = edit_blog_form.author.data
        post.img_url = edit_blog_form.img_url.data
        post.body = edit_blog_form.body.data
        db.session.commit()
        return redirect(url_for(f'display_post', post_id=post_id))

    return render_template("make-post.html", form=edit_blog_form, h1_text="Edit Post", year=current_year)


@app.route("/delete/<int:post_id>")
def delete(post_id):
    BlogPost.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/about")
def about():
    return render_template("about.html", year=current_year)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message_body = request.form['message_body']
        print(f"name: {name}\nemail: {email}\nphone: {phone}\nmessage: {message_body}")
        message = MIMEMultipart("alternative")
        message["Subject"] = "New contact message from blog"
        message["From"] = FROM_ADDR
        message["To"] = TO_ADDR
        text = f"name: {name}\nemail: {email}\nphone: {phone}\nmessage: {message_body}"
        html = f"""
        <html>
          <head></head>
          <body>
            <p>
                {name}<br>
                {email}<br>
                {phone}<br>
                {message_body}<br>
            </p>
          </body>
        </html>
        """

        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        message.attach(part1)
        message.attach(part2)

        with smtplib.SMTP(HOST_EMAIL, port=587) as connection:
            connection.starttls()
            connection.login(user=FROM_ADDR, password=FROM_ADDR_APP_PASSWORD)
            connection.sendmail(
                from_addr=FROM_ADDR,
                to_addrs=TO_ADDR,
                msg=message.as_string()
            )
        return render_template("contact.html", year=current_year, msg_sent=True)
    return render_template("contact.html", year=current_year, msg_sent=False)


if __name__ == "__main__":
    app.run(debug=True)
