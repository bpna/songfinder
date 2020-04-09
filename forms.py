from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    lyric = StringField('Search term:', validators=[DataRequired()])
    submit = SubmitField('submit')
