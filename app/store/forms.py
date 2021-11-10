from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.core import BooleanField, FloatField
from wtforms.fields.html5 import IntegerField
from wtforms.fields.simple import TextField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed

class ProductForm(FlaskForm):
    name = StringField('Nombre del producto', validators=[DataRequired()])
    price = FloatField('Precio de venta', validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired()])
    image = FileField('Imagen del producto', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Sólo se permiten imágenes')
    ])
    description = TextField('Descripción del producto', validators=[DataRequired()])
    fanmade = BooleanField('¿Fanmade?')
    submit = SubmitField('Guardar')