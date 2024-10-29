from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class LocationForm(FlaskForm):
    location = StringField("Enter any city in the world: ", validators=[DataRequired()])
    submit = SubmitField(label="Collect Weather Data")