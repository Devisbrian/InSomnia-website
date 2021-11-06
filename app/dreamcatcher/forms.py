from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, URL
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.core import SelectField

class PhotocardDbForm(FlaskForm):
    album = SelectField('Álbum', choices=[], validators=[DataRequired()])
    member = SelectField('Miembro', choices=[], validators=[DataRequired()])
    pc_type = SelectField('Versión de Photocard', choices=[], validators=[DataRequired()])
    pc_name = StringField('Nombre de Photocard', validators=[DataRequired()])
    photocard_image = FileField('Imagen', validators=[FileAllowed(['jpg', 'png'],'Sólo se permiten imágenes JPG y PNG')])
    submit = SubmitField('Guardar')
    
class AlbumTypeForm(FlaskForm):
    album = SelectField('Seleccionar álbum', choices=[], validators=[DataRequired()])
    pc_type = StringField('Crear versión de photocard', validators=[DataRequired()])
    submit = SubmitField('Guardar')
    
class AlbumForm(FlaskForm):
    album = StringField('Álbum', validators=[DataRequired()])
    date = DateField('Fecha de lanzamiento', format='%Y-%m-%d', validators=[DataRequired()])
    songs = TextAreaField('Canciones')
    producers = TextAreaField('Productores')
    spotify = StringField('Link a Spotify', validators=[URL(require_tld=True)])
    youtube = StringField('Link a Youtube', validators=[URL(require_tld=True)])
    album_image = FileField('Imagen del álbum', validators=[FileAllowed(['jpg', 'png', 'jpeg'],'Sólo se permiten imágenes JPG y PNG')])
    submit = SubmitField('Guardar')

class MemberDcForm(FlaskForm):
    member = StringField('Miembro', validators=[DataRequired()])
    submit = SubmitField('Guardar')