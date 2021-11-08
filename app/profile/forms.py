from flask import current_app
from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.core import SelectField, SelectMultipleField
from wtforms.validators import DataRequired

class AddProfilePic(FlaskForm):
    profile_pic = FileField('Foto de perfil', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Sólo se permiten imágenes'), DataRequired()
    ])
    submit = SubmitField('Subir')

class AddAlbums(FlaskForm):
    albums = SelectMultipleField('Agregar álbumes', choices=[])
    submitA = SubmitField('Guardar')

class AddPhotocards(FlaskForm):
    album = SelectField('Seleccione álbum', choices=[])
    album_type = SelectField('Seleccione la versión de photocard', choices=[])
    members = SelectMultipleField('Seleccione las miembros', choices=[])
    submitP = SubmitField('Guardar')

