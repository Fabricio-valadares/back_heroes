from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class UsersModel(db.Model):
    __tablename__ = "usersmodel"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    user_caso = db.relationship("Casos", back_populates="caso_user")

    @property
    def password(self):
        raise TypeError("key cannot be accessed")
    
    @password.setter
    def password(self, send_password):
        password_in_hash = generate_password_hash(send_password)
        self.password_hash = password_in_hash
    
    def check_password(self, check_password_args):
        return check_password_hash(self.password_hash, check_password_args)