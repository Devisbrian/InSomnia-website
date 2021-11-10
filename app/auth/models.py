from flask_login import UserMixin
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

from app import db

user_exchange_interest = db.Table('user_exchange_interest', 
    db.Column('user_id', db.Integer, db.ForeignKey('blog_user.id')),
    db.Column('pc_exchange_id', db.Integer, db.ForeignKey('photocard_exchange.id')),
)

user_albums = db.Table('user_albums',
    db.Column('user_id', db.Integer, db.ForeignKey('blog_user.id')),
    db.Column('album_id', db.Integer, db.ForeignKey('album.id')),
)

user_photocards = db.Table('user_photocards',
    db.Column('user_id', db.Integer, db.ForeignKey('blog_user.id')),
    db.Column('photocard_id', db.Integer, db.ForeignKey('photocard_db.id')),
)

class User(db.Model, UserMixin):

    __tablename__ = 'blog_user'

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    username = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id', ondelete='SET NULL'))
    phone = db.Column(db.String(15))
    birthday = db.Column(db.Date)
    is_admin = db.Column(db.Boolean, default=False)
    is_staff = db.Column(db.Boolean, default=False)
    confirm = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(128), nullable=False)
    profile_pic_name = db.Column(db.String)
    facebook = db.Column(db.String(80))
    twitter = db.Column(db.String(80))
    instagram = db.Column(db.String(80))
    exchange = db.relationship('PhotocardExchange', backref=db.backref('user', lazy=True))
    exchange_interested = db.relationship('PhotocardExchange', secondary=user_exchange_interest, backref=db.backref('users_interested', lazy='dynamic'))
    albums = db.relationship('Album', secondary=user_albums, backref=db.backref('users_own', lazy='dynamic'))
    photocards = db.relationship('PhotocardDb', secondary=user_photocards, backref=db.backref('users_own', lazy='dynamic'))

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
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    #@staticmethod
    #def get_by_pc():
    #    return User.query.

class Cities(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    users = db.relationship('User', backref=db.backref('city', lazy=True))

    def __repr__(self):
        return f'<City {self.name}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Cities.query.all()

    @staticmethod
    def get_by_id(id):
        return Cities.query.get(id)

    @staticmethod
    def get_by_name(name):
        return Cities.query.filter_by(name=name).first()