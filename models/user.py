from models.db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from flask_login import UserMixin

''' NOTES:
In the SQLAlchemy documentation the PEP 484 annotation would define the posts column in
the table below as...

    posts: Mapped[List["BlogPost"]] = relationship(back_populates="author")

which is the "modern form of declarative mapping. However, "BlogPost" will give a warning that 
it is an unresolved reference even though the code will work. 
https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#declarative-vs-imperative-forms
You would also need to import List for the above mapping to work.

    from typing import List

You can get rid of the warning highlight by importing the other model. In this case...

    from models.blogpost import BlogPost
    
and you would have to import User in the blogpost.py file. The problem with this is you'll have circular
imports and the code won't run (main.py imports both models as well).

You can get around the circular imports by importing TYPE_CHECKING in each model...

    from typing import List, TYPE_CHECKING
    
and then...

    if TYPE_CHECKING:
        from models.blogpost import BlogPost
    
https://mypy.readthedocs.io/en/stable/runtime_troubles.html#import-cycles


which feels a bit hacky to me. You could have both models in the same file to avoid this, but I've read
it's recommended to keep models in separate files. This is why I've chosen to use the "classic" version
for the 'posts' column below without annotations even though the syntax is inconsistent.
'''


class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comment", back_populates="author")

    @property
    def is_admin(self):
        if self.id == 1:
            return True
        return False
