from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class UsernameForm(FlaskForm):
    username = StringField('Username')
    submit = SubmitField('Enter')
