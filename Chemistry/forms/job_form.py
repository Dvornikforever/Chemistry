from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired()])
    job = StringField('Работа')
