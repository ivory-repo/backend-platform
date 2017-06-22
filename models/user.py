from werkzeug.security import generate_password_hash, check_password_hash

from db import db

class UserModel(db.Model):

    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    pw_hash = db.Column(db.String(255))
    active = db.Column(db.Boolean(create_constraint=True))

    def __init__(self, username, password, active):
        self.username = username
        self.pw_hash  = generate_password_hash(password)
        self.active = active
    
    def check_password(self, password):
        return check_password_hash(self.pw_hash , password)
    
    def json(self):
        return {'username': self.username, 'active': self.active}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
