from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_wtf import FlaskForm


class StudentForm(FlaskForm):
    name = StringField('Name', validators=[Required()])
    surname = StringField('Surname', validators=[Required()])
    create = SubmitField('Create')


class DisciplineForm(FlaskForm):
    title = StringField('Title', validators=[Required()])
    create = SubmitField('Create')
    