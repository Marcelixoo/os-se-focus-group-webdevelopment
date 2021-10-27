from flask import render_template, request, url_for, redirect, flash, request, jsonify, json, Blueprint, session
from flask_login import current_user, login_required
from great_project import db, login_manager
import datetime
from great_project.event.forms import EventRegistration
from great_project.models import Atleta, Academy, Belt, Gender, Event, Age_division, Registration, Weight, Weight_age_division_gender, Age_division_belt
from great_project.event.utils import age_division_choices, generate_confirmation_token, confirm_token, send_email

# login manager to know the current user


@login_manager.user_loader
def load_user(atleta_id):
    return Atleta.query.get(int(atleta_id))


emojis = Blueprint('emojis', __name__)

# route for next event


@emojis.route('/evento1')
def evento1():
    return render_template('evento1.html', page_title="Evento")
