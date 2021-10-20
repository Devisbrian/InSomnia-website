from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

from app import db

class User(db.Model, UserMixin):

    __tablename__ = 'blog_user'

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    username = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    city = db.Column(db.String(80))
    phone = db.Column(db.String(15))
    birthday = db.Column(db.Date)
    is_admin = db.Column(db.Boolean, default=False)
    is_staff = db.Column(db.Boolean, default=False)
    confirm = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(128), nullable=False)
    exchange = db.relationship('PhotocardExchange', backref=db.backref('user', lazy=True))

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
        
    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter(User.email.ilike("%"+email+"%")).first()
    
    @staticmethod
    def get_by_username(username):
        return User.query.filter(User.username.ilike("%"+username+"%")).first()