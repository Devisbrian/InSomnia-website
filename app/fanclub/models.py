from app import db

class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    image_name = db.Column(db.String(256))
    date = db.Column(db.Date)
    photos = db.relationship('Gallery', backref='event', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Event {self.name}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Events.query.all()

    @staticmethod
    def get_by_id(id):
        return Events.query.get(id)

    @staticmethod
    def get_by_name(name):
        return Events.query.filter_by(name=name).first()


class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.String)
    event_id = db.Column(db.ForeignKey('events.id', ondelete='CASCADE'))
    #event

    def __repr__(self):
        return f'<photo {self.id} from {self.event_id}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Gallery.query.all()

    @staticmethod
    def get_by_id(id):
        return Gallery.query.get(id)

    @staticmethod
    def get_by_event(event_id):
        return Gallery.query.filter_by(event_id=event_id).all()