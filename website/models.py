from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # notes = db.relationship("Note")
    entries = db.relationship("BookEntry")


class BookEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    author = db.Column(db.String(150))
    is_series = db.Column(db.Boolean)
    series = db.Column(db.String(150))
    num_in_series = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    rating = db.Column(db.Integer)
    review = db.Column(db.String(10000))
    cover = db.Column(db.String(300))
    genre = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
