from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.validators import DataRequired
from wtforms.fields.core import SelectField
from ..const import MEMBER_LIST

class CommentForm(FlaskForm):
    content = TextAreaField('Contenido', validators=[DataRequired(), ])
    submit = SubmitField('Comentar')

class ExchangeForm(FlaskForm):
    album_from = SelectField('Álbum', choices=[], validators=[DataRequired(), ])
    member_from = SelectField('Miembro', choices=MEMBER_LIST, validators=[DataRequired(), ])
    pc_type_from = SelectField('Versión photocard', choices=[], validators=[DataRequired(), ])
    album_to = SelectField('Álbum', choices=[], validators=[DataRequired(), ])
    member_to = SelectField('Miembro', choices=MEMBER_LIST, validators=[DataRequired(), ])
    pc_type_to = SelectField('Versión photocard', choices=[], validators=[DataRequired(), ])
    submit = SubmitField('Crear')