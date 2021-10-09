from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.core import SelectField

MEMBER_LIST = [('','Seleccione'),('JiU','JiU'),('SuA','SuA'),('Siyeon','Siyeon'),('Handong','Handong'),('Yoohyeon','Yoohyeon'),('Dami','Dami'),('Gahyeon','Gahyeon')]

class PostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=128)])
    description = TextAreaField('Encabezado', validators=[DataRequired()])
    content = TextAreaField('Contenido')
    post_image = FileField('Imagen', validators=[
        FileAllowed(['jpg', 'png'], 'Sólo se permiten imágenes')
    ])
    submit = SubmitField('Enviar')
    

class UserAdminForm(FlaskForm):
    is_admin = BooleanField('Administrador')
    is_staff = BooleanField('Staff')
    submit = SubmitField('Guardar')
    
class PhotocardDbForm(FlaskForm):
    album = SelectField('Álbum', choices=[], validators=[DataRequired()])
    member = SelectField('Miembro', choices=MEMBER_LIST, validators=[DataRequired()])
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
    album_image = FileField('Imagen del álbum', validators=[FileAllowed(['jpg', 'png'],'Sólo se permiten imágenes JPG y PNG')])
    submit = SubmitField('Guardar')