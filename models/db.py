from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


# Create database
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)