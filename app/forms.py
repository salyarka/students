from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_wtf import FlaskForm


class StudentForm(FlaskForm):
    name = StringField('Name', validators=[Required()])
    create = SubmitField('Create')
    update = SubmitField('Update')


class DisciplineForm(FlaskForm):
    title = StringField('Title', validators=[Required()])
    create = SubmitField('Create')
    update = SubmitField('Update')


class SearchForm(FlaskForm):
    name = StringField('Student name', validators=[Required()])
    search = SubmitField('Search')
