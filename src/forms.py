from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class LocationForm(FlaskForm):
    """
    Form for entering a location to collect weather data.

    Attributes:
        location (StringField): Input field for city name, required.
        submit (SubmitField): Button to submit the form.
    """
    location = StringField("Enter any city in the world: ", validators=[DataRequired()])
    submit = SubmitField(label="Collect Weather Data")