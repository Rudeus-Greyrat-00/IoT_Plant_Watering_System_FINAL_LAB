from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField

class NewHubForm(FlaskForm):
    name = StringField('name')
    desired_humidity = StringField('desired_humidity')
    watering_frequency = StringField('watering_frequency')
    submit = SubmitField('submit')