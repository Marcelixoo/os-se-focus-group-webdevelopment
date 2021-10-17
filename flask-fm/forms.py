# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SongForm(FlaskForm):
    title = StringField(label="Song Title:", validators=[DataRequired()])
    artist = StringField(label="Artist:", validators=[DataRequired()])
    submit = SubmitField("Add Song")
