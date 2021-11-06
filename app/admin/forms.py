from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed

class PostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=128)])
    description = StringField('Encabezado', validators=[DataRequired()])
    content = TextAreaField('Contenido')
    post_image = FileField('Imagen', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Sólo se permiten imágenes')
    ])
    submit = SubmitField('Enviar')
    

class UserAdminForm(FlaskForm):
    is_admin = BooleanField('Administrador')
    is_staff = BooleanField('Staff')
    submit = SubmitField('Guardar')

class CityForm(FlaskForm):
    name = StringField('Ciudad', validators=[DataRequired()])
    submit = SubmitField('Guardar')