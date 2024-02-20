from models.db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, ForeignKey

''' NOTES:
In the SQLAlchemy documentation the PEP 484 annotation would define the posts column in
the table below as...

    author: Mapped["User"] = relationship("User", back_populates="posts")

which is the "modern form of declarative mapping. However, "User" will give a warning that 
it is an unresolved reference even though the code will work. 
https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#declarative-vs-imperative-forms

You can get rid of the warning highlight by importing the other model. In this case...

    from models.user import User

and you would have to import BlogPost in the user.py file. The problem with this is you'll have circular
imports and the code won't run (main.py imports both models as well).

You can get around the circular imports by importing TYPE_CHECKING in each model...

    from typing import TYPE_CHECKING

and then...

    if TYPE_CHECKING:
        from models.user import User

https://mypy.readthedocs.io/en/stable/runtime_troubles.html#import-cycles


which feels a bit hacky to me. You could have both models in the same file to avoid this, but I've read
it's recommended to keep models in separate files. This is why I've chosen to use the "classic" version
for the 'posts' column below without annotations even though the syntax is inconsistent.
'''


class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author = relationship("User", back_populates="posts")

