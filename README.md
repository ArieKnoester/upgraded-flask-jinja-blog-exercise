# upgraded-flask-jinja-blog-exercise

Work in progress.

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

### Notes:
- While flask-ckeditor's documentation states it has a 'cleanify' method for HTML sanitizing, it is 
apparently missing as of version 0.5.1. Version 0.5.2 adds it back, but there is no release date for it
as of 2024-02-14 (https://flask-ckeditor.readthedocs.io/en/latest/changelog.html). I looked into Bleach, 
but it has been depreciated (https://pypi.org/project/bleach/). The GitHub repo for Bleach lead me to 
nh3 (https://nh3.readthedocs.io/en/latest/).


- The course requirements specified that the user with id == 1 (first person to register) is the sole 
admin and that the current_user's id should be checked to secure routes and display buttons for those 
routes. While I appreciated reviewing custom decorators, I do not like this approach. For now, I created
a method in the User class as an @property as a quick compromise. I may update the User table and add an
'is_admin' boolean column as that is the typical way. It even states in the course materials,
  > _"In the future, maybe we will want to invite other users to write posts in the blog and grant them
      the admin privileges."_

- The course requirements specified that only a logged-in user should be able to comment on posts. If 
a user is not logged-in, and they try to submit a comment they should receive a flask message informing 
them and are redirected to the Login route. In my opinion, I think this design is bad UX. The comment 
field is a ckeditor field, and they could have spent a lot of time formatting their comment. So I chose
a different approach. For unauthenticated users, the comment form is not rendered. The text "Want to 
comment on this post? Register or Login!" is displayed in its place.
  
### TODO:
- ~~Relate User table to BlogPost table.~~
- ~~Implement a comments form and db table.~~
- ~~Relate comments table to other tables.~~
- ~~Only registered users can leave comments on posted blogs.~~
- Make all comments on a post visible.
- Implement user avatar.