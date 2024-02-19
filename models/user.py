from models.db import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))

    @property
    def is_admin(self):
        if self.id == 1:
            return True
        return False
