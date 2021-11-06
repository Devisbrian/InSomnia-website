from app import db
import datetime

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image_name = db.Column(db.String(100))
    description = db.Column(db.Text)
    fanmade = db.Column(db.Boolean)
    rate = db.Column(db.Float)
    #product_in = db.relationship('Cart_Product', backref='product', lazy='dynamic')

    def __repr__(self):
        return f'<Product {self.name}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Product.query.all()

    @staticmethod
    def get_by_id(id):
        return Product.query.get(id)

""" class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('blog_user.id'))
    date = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    products = db.relationship('Cart_Product', backref='cart', lazy='dynamic')

    def __repr__(self):
        return f'<Cart {self.id} user {self.user_id}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
            
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Cart.query.all()

    @staticmethod
    def get_by_id(id):
        return Cart.query.get(id) """

""" class Cart_Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
    #product
    #cart

    def __repr__(self):
        return f'<Cart_Product {self.id}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
            
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Cart_Product.query.all()

    @staticmethod
    def get_by_id(id):
        return Cart_Product.query.get(id)
    
    @staticmethod
    def get_by_cart_id(cart_id):
        return Cart_Product.query.filter_by(cart_id=cart_id) """