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
- gunicorn
- psycopg2-binary

### Notes:
- While flask-ckeditor's documentation states it has a 'cleanify' method for HTML sanitizing, it is 
apparently missing as of version 0.5.1. Version 0.5.2 adds it back, but there is no release date for it
as of 2024-02-14 (https://flask-ckeditor.readthedocs.io/en/latest/changelog.html). I looked into Bleach, 
but it has been depreciated (https://pypi.org/project/bleach/). The GitHub repo for Bleach lead me to 
nh3 (https://nh3.readthedocs.io/en/latest/).


- The course requirements specified that the user with id == 1 (first person to register) is the sole 
admin and that the current_user's id should be checked to secure routes and display buttons for those 
routes. While I appreciated reviewing custom decorators, I do not like this approach. For now, I created
a method in the User class as a @property as a quick compromise. I may update the User table and add an
'is_admin' boolean column as that is the typical way. It even states in the course materials,
  > _"In the future, maybe we will want to invite other users to write posts in the blog and grant them
      the admin privileges."_

- The course requirements specified that only a logged-in user should be able to comment on posts. If 
a user is not logged-in, and they try to submit a comment they should receive a flash message informing 
them and are redirected to the Login route. In my opinion, I think this design is bad UX. The comment 
field is a ckeditor field, and they could have spent a lot of time formatting their comment. So I chose
a different approach. For unauthenticated users, the comment form is not rendered. The text "Want to 
comment on this post? Register or Login!" is displayed in its place.
  
### TODO:
- ~~Relate User table to BlogPost table.~~
- ~~Implement a comments form and db table.~~
- ~~Relate comments table to other tables.~~
- ~~Only registered users can leave comments on posted blogs.~~
- ~~Make all comments on a post visible.~~
- ~~Implement Gravatar.~~
- ~~Fix hacky styling for alternate text to CommentForm.~~
- ~~Remove any TODOs and unneeded commented out HTML.~~
- ~~gunicorn Procfile.~~
- ~~Fix missing csrf token on contact form causing Bad Request response.~~
- ~~Replace template's validation for contact form.~~
- ~~.gitignore.~~
- ~~Fix issue with newly submitted comment not displaying on the post.~~
- ~~Change home page header and subhead.~~
- Decide if I want to keep the social media links in the footer. They are not functional, but they look
nice.
- Add the ability for users to edit their comments?
- Links to an author of a post are not functional. Remove the links as I likely won't implement any
sort of profile page or any page which displays a specific user's site content.
- Add 'is_admin' column to the User table? If I do this, I need to implement some route/page where the
admin can make other users an admin. Also need to make it so that they can only post/edit/delete their 
own content. It's unlikely I will do this. I need to move on to other projects.
- Deploy to Render or some other free hosting site. I don't intend to start blogging, but it would be
nice to have this running somewhere after all the time I put into it.