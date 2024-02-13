# Templates used: https://startbootstrap.com/previews/clean-blog
# Other template sites. Not used here, but links added for reference:
# https://bootstrapmade.com/
# https://getbootstrap.com/docs/5.0/examples/
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from models.blogpost import BlogPost, db
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


current_year = datetime.datetime.now().year
app = Flask(__name__)
Bootstrap5(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.secret_key = SECRET_KEY
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    all_posts = db.session.execute(db.select(BlogPost)).scalars()
    return render_template("index.html", posts=all_posts, year=current_year)


@app.route("/post/<int:post_id>")
def display_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    return render_template("post.html", post=post, year=current_year)


# TODO: add_new_post() to create a new blog post

# TODO: edit_post() to change an existing blog post

# TODO: delete_post() to remove a blog post from the database

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
