from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Required, NumberRange
from flask_wtf import FlaskForm


req_msg = 'This field is required.'


class StudentForm(FlaskForm):
    name = StringField('Name', validators=[Required(req_msg)])
    surname = StringField('Surname', validators=[Required(req_msg)])
    create = SubmitField('Create')
    update = SubmitField('Update')


class DisciplineForm(FlaskForm):
    title = StringField('Title', validators=[Required(req_msg)])
    create = SubmitField('Create')
    update = SubmitField('Update')


# class ScoreForm(FlaskForm):
#     score = IntegerField(
#         'Score', validators=[
#             Required(req_msg),
#             NumberRange(1, 5, 'Value can be a number from 1 to 5')
#         ]
#     )
#     set_score = SubmitField('Set')
    