from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, MultipleFileField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed

class EventGalleryForm(FlaskForm):
    name = StringField('Nombre del evento', validators=[DataRequired()])
    event_image = FileField('Foto principal', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Sólo se permiten imágenes'), DataRequired()
    ])
    date = DateField('Fecha del evento', format='%Y-%m-%d', validators=[DataRequired()])
    gallery_images = MultipleFileField('Foto principal', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Sólo se permiten imágenes'), DataRequired()
    ])
    submit = SubmitField('Guardar')