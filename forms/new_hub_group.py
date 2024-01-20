from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField

class NewHubGroupForm(FlaskForm):
    name = StringField('name')
    location = StringField('location')
    submit = SubmitField('submit')