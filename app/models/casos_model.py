from sqlalchemy.orm import backref, relationship
from . import db

class Casos(db.Model):
    __tablename__ = "casos"

    caso_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    decription = db.Column(db.Text, nullable=False)
    value = db.Column(db.Integer, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey("usersmodel.user_id"))
    caso_user = db.relationship("UsersModel", back_populates="user_caso")
