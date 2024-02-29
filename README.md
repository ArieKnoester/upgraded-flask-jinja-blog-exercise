# upgraded-flask-jinja-blog-exercise

Deployed at https://some-dudes-blog.onrender.com
(Free Render sites spin down with inactivity which may delay requests to the site)
(Database will expire May 29, 2024)

## Description

An updated version of a simple blog exercise at https://github.com/ArieKnoester/flask-jinja-blog-exercise

Changes from the original include:
- Start Bootstrap's clean blog template (https://startbootstrap.com/previews/clean-blog)
- flask_bootstrap
- flask_wtf
- flask_sqlalchemy
- flask_ckeditor
- nh3
- flask_login
- flask_gravatar
- gunicorn
- psycopg2-binary

### Notes:
- While flask-ckeditor's documentation states it has a 'cleanify' method for HTML sanitizing, it is 
apparently missing as of version 0.5.1. Version 0.5.2 adds it back, but there is no release date for it
as of 2024-02-14 (https://flask-ckeditor.readthedocs.io/en/latest/changelog.html). I looked into Bleach, 
but it has been depreciated (https://pypi.org/project/bleach/). The GitHub repo for Bleach lead me to 
nh3 (https://nh3.readthedocs.io/en/latest/).

- The course requirements specified that only a logged-in user should be able to comment on posts. If 
a user is not logged-in, and they try to submit a comment they should receive a flash message informing 
them and are redirected to the Login route. In my opinion, I think this design is bad UX. The comment 
field is a ckeditor field, and they could have spent a lot of time formatting their comment only to lose
it when redirected. I chose a different approach. For unauthenticated users, the comment form is not 
rendered. The text "Want to comment on this post? Register or Login!" is displayed in its place.
