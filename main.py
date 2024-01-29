# Templates used: https://startbootstrap.com/previews/clean-blog
# Other template sites. Not used here, but links added for reference:
# https://bootstrapmade.com/
# https://getbootstrap.com/docs/5.0/examples/

# Fake blog posts were created at: https://www.npoint.io/
# Newly created 'APIs' go away after a while. A new one may need
# to be created if the request returns null. Data for these fake
# posts can be found in the static/assets/data directory.
from flask import Flask, render_template, request
import requests
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


def request_dummy_blog_posts():
    dummy_blogs_response = requests.get("https://api.npoint.io/c1b18044c1eb6b6d0eb1")
    dummy_blogs_response.raise_for_status()
    dummy_blogs = dummy_blogs_response.json()
    return dummy_blogs


posts_data = request_dummy_blog_posts()
current_year = datetime.datetime.now().year
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", posts=posts_data, year=current_year)


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


@app.route("/post/<int:post_id>")
def display_post(post_id):
    post = posts_data[post_id]
    return render_template("post.html", post=post, year=current_year)


if __name__ == "__main__":
    app.run(debug=True)
