from . import mongo_db as db
from flask_login import UserMixin
from sqlalchemy.sql import func


# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class BookEntry(db.Document):
    title = db.StringField(max_length=150)
    author = db.StringField(max_length=150)
    is_series = db.BooleanField()
    series = db.StringField(max_length=150)
    num_in_series = db.FloatField()
    date = db.DateTimeField()
    rating = db.IntField()
    review = db.StringField(max_length=10000)
    cover = db.StringField(max_length=300)
    genre = db.StringField(max_length=150)
    user_id = db.ObjectIdField()
    is_reread = db.BooleanField()


class User(db.Document, UserMixin):
    email = db.StringField(max_length=150)
    password = db.StringField(max_length=150)
    first_name = db.StringField(max_length=150)
    # notes = db.relationship("Note")
    entries = db.ListField(db.Document())

