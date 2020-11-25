from .. import db


class User(db.Document):
    name = db.StringField()
    email = db.EmailField()
    password = db.StringField()
