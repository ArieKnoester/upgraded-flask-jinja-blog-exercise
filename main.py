# Templates used: https://startbootstrap.com/previews/clean-blog
# Other template sites. Not used here, but links added for reference:
# https://bootstrapmade.com/
# https://getbootstrap.com/docs/5.0/examples/

# Fake blog posts were created at: https://www.npoint.io/
# Newly created 'APIs' go away after a while. A new one may need
# to be created if the request returns null. Data for these fake
# posts can be found in the static/assets/data directory.
from flask import Flask, render_template
import requests
import datetime


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


@app.route("/contact")
def contact():
    return render_template("contact.html", year=current_year)


@app.route("/post/<int:post_id>")
def display_post(post_id):
    post = posts_data[post_id]
    return render_template("post.html", post=post, year=current_year)


if __name__ == "__main__":
    app.run(debug=True)
