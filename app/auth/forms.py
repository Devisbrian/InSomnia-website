from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectMultipleField
from wtforms.fields.html5 import DateField
from wtforms.fields.core import SelectField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo

class SignupForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired(), Regexp('^\w+$', message="No se permiten carácteres especiales"), Length(max=20)])
    name = StringField('Nombres', validators=[DataRequired(), Length(max=64)])
    lastname = StringField('Apellidos', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Contraseña', validators=[DataRequired(), EqualTo('password_confirm', message='Passwords must match')])
    password_confirm = PasswordField('Confirmar contraseña', validators=[DataRequired()])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email(message="El correo debe ser de la forma ejemplo@ejemplo.com")])
    city = SelectField('Ciudad', choices=[('','Seleccione'),('Bogotá','Bogotá'),('Medellín','Medellín'),('Cali','Cali'),('Barranquilla','Barranquilla'),('Cartagena','Cartagena'),('Otra','Otra')], validators=[DataRequired()])
    phone = StringField('Celular', validators=[DataRequired(), Length(min=10,max=10,message="El número de celular debe ser de 10 dígitos")])
    birthday = DateField('Fecha de nacimiento', format='%Y-%m-%d', validators=[DataRequired()])
    bias = SelectMultipleField('Bias', choices=[], validators=[DataRequired()])
    submit = SubmitField('Registrarse')


class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Iniciar sesión')
