from flask import url_for
from slugify import slugify
from sqlalchemy.exc import IntegrityError
import datetime
from sqlalchemy import desc

from app import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('blog_user.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(256), nullable=False)
    title_slug = db.Column(db.String(256), unique=True, nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    image_name = db.Column(db.String)
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan', order_by='asc(Comment.created)')

    def __repr__(self):
        return f'<Post {self.title}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        if not self.title_slug:
            self.title_slug = slugify(self.title)

        saved = False
        count = 0
        while not saved:
            try:
                db.session.commit()
                saved = True
            except IntegrityError:
                db.session.rollback()
                db.session.add(self)
                count += 1
                self.title_slug = f'{slugify(self.title)}-{count}'
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
        
    @staticmethod
    def get_by_id(id):
        return Post.query.get(id)

    @staticmethod
    def get_by_slug(slug):
        return Post.query.filter_by(title_slug=slug).first()

    @staticmethod
    def get_all():
        return Post.query.all()
    
    @staticmethod
    def all_paginated(page=1, per_page=20):
        return Post.query.order_by(Post.created.desc()).\
            paginate(page=page, per_page=per_page, error_out=False)
        

# Comentar los posts
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('blog_user.id', ondelete='SET NULL'))
    user_username = db.Column(db.String)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    content = db.Column(db.Text)

    def __init__(self, content, user_id=None, user_username=user_username, post_id=None):
        self.content = content
        self.user_id = user_id
        self.user_username = user_username
        self.post_id = post_id

    def __repr__(self):
        return f'<Comment {self.content}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_post_id(post_id):
        return Comment.query.filter_by(post_id=post_id).all()
    
    
class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    album = db.Column(db.String(256), nullable=False)
    album_image_name = db.Column(db.String, nullable=False)
    date = db.Column(db.Date)
    songs = db.Column(db.Text)
    producers = db.Column(db.Text)
    spotify = db.Column(db.String)
    youtube = db.Column(db.String)
    
    def __repr__(self):
        return f'<Album {self.album}>'
    
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    @staticmethod
    def get_by_id(id):
        return Album.query.get(id)
    
    @staticmethod
    def get_all():
        return Album.query.all()


class AlbumType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    album = db.Column(db.String(256), nullable=False)
    pc_type = db.Column(db.String(256), nullable=False)
    
    def __repr__(self):
        return f'<AlbumType {self.album}>'
    
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    @staticmethod
    def get_by_id(id):
        return AlbumType.query.get(id)
    
    @staticmethod
    def get_all():
        return AlbumType.query.all()
    
    @staticmethod
    def get_by_pctype(pc_type):
        return AlbumType.query.filter_by(pc_type=pc_type).all()
    
    @staticmethod
    def get_by_album(album):
        return AlbumType.query.filter_by(album=album).all()

    @staticmethod
    def get_album_distinct():
        return AlbumType.query.distinct(AlbumType.album)
    

class PhotocardDb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    album = db.Column(db.String(256), nullable=False)
    member = db.Column(db.String(256), nullable=False)
    pc_type = db.Column(db.String(256), nullable=False)
    pc_name = db.Column(db.String(256), nullable=False, unique=True)
    pc_image_name = db.Column(db.String)
    
    def __repr__(self):
        return f'<PhotocardDb {self.pc_name}>'
    
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    @staticmethod
    def get_by_id(id):
        return PhotocardDb.query.get(id)
    
    @staticmethod
    def get_all():
        return PhotocardDb.query.all()

    @staticmethod
    def get_albums():
        return PhotocardDb.query.distinct(PhotocardDb.album)

    @staticmethod
    def get_type():
        return PhotocardDb.query.distinct(PhotocardDb.pc_type)
    
    @staticmethod
    def get_filtered(album, pc_type, member):
        return PhotocardDb.query.filter_by(album=album).filter_by(pc_type=pc_type).filter_by(member=member).first()
    

class PhotocardExchange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('blog_user.id', ondelete='CASCADE'))
    user_username = db.Column(db.String)
    pc_id_from = db.Column(db.Integer)
    album_from = db.Column(db.String(256), nullable=False)
    member_from = db.Column(db.String(256), nullable=False)
    pc_type_from = db.Column(db.String(256), nullable=False)
    pc_name_from = db.Column(db.String(256), nullable=False, unique=True)
    pc_image_name_from = db.Column(db.String)
    pc_id_to = db.Column(db.Integer)
    album_to = db.Column(db.String(256), nullable=False)
    member_to = db.Column(db.String(256), nullable=False)
    pc_type_to = db.Column(db.String(256), nullable=False)
    pc_name_to = db.Column(db.String(256), nullable=False, unique=True)
    pc_image_name_to = db.Column(db.String)

    def __repr__(self):
        return f'<PhotocardExchange {self.id}>'
    
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    @staticmethod
    def get_by_id(id):
        return PhotocardExchange.query.get(id)
    
    @staticmethod
    def get_all():
        return PhotocardExchange.query.order_by(PhotocardExchange.created.desc()).all()