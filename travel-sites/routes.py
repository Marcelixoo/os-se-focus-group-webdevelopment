from flask import request, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from models import User, Post
from forms import RegistrationForm, LoginForm, DestinationForm


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm(meta={'csrf': False})

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).one()
        except Exception:
            flash('Invalid username and password combination')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash('Logged in successfully')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('login'))

    form = RegistrationForm(meta={'csrf': False})

    if form.validate_on_submit():
        try:
            User.create(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data
            )
        except Exception:
            flash('Email or Username already taken!')
            return redirect(url_for('register'))
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    if current_user.username != username:
        return redirect(url_for('login'))
    user = User.query.filter_by(username=current_user.username).first()
    posts = Post.query.filter_by(user_id=user.id) or []

    form = DestinationForm(meta={'csrf': False})

    if request.method == 'POST' and form.validate():
        new_destination = Post(
            city=form.city.data,
            country=form.country.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(new_destination)
        db.session.commit()
    else:
        for field, errors in form.errors.items():
            flash(f"[{field}] {''.join(errors)}")
    return render_template('user.html', user=user, posts=posts, form=form)

@app.route('/')
def index():
    posts = Post.query.all() or []
    return render_template('landing_page.html', posts=posts)
