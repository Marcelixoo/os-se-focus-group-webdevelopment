from flask import Flask, render_template, request, flash
from flask.helpers import url_for
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email
from werkzeug.security import generate_password_hash, check_password_hash

# from my_fav_emojis import create_app  # noqa: F401

# app = create_app()

# if __name__ == "__main__":
#     app.run(debug=True)


app = Flask(__name__)

app.config['FLASK_APP'] = 'app'
app.config['FLASK_ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emojis_library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'you-will-never-guess'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


'''
Requirements:

1. Replace HTML strings with templates.
2. Save an initial collection of emojis to the database using a one-time script.
3. Allow the upload of new emojis.
'''


class Emoji(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    size = 512

    def __repr__(self) -> str:
        return "https://emojiapi.dev/api/v1/{}/{}.png".format(self.name, self.size)


class NewEmojiForm(FlaskForm):
    name = StringField(label="Emoji Name", validators=[DataRequired()])
    submit = SubmitField("Add Emoji")


@app.route('/')
@login_required
def index():
    emojis = Emoji.query.all()
    return render_template('emojis.html', emojis=emojis)


@app.route('/emoji', methods=["POST"])
def add_emoji():
    form = NewEmojiForm(csrf_enabled=False)
    if request.method == 'POST' and form.validate():
        new_song = Emoji(emoji=form.name.data)
        db.session.add(new_song)
        try:
            db.session.commit()
        except:
            db.session.rollback()
    elif form.errors:
        flash(form.errors)
    return redirect(url_for('index'))


@app.route('/emojis/<name>')
@login_required
def emoji(name):
    emoji = Emoji.query.filter(Emoji.name == name).one()
    return render_template('emoji.html', emoji=emoji)


class LoginForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    password_confirmation = PasswordField(label="Repeat Password",
                                          validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm(meta={'csrf': False})

    if form.validate_on_submit():
        email = form.email.data
        try:
            user = User.query.filter_by(email=email).one()
            if not user.check_password(form.password.data):
                flash("Invalid password")
            else:
                flash("Logged in successfully!")
                login_user(user)
                return redirect(url_for('index'))
        except ValueError:
            flash(f"Could not find user with email: {email}")
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


class User(UserMixin, db.Model):
    id = id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def create(self, email, password):
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password_to_check):
        return check_password_hash(self.password, password_to_check)

    def __repr__(self):
        return '<User {}>'.format(self.email)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm(meta={'csrf': False})

    if form.validate_on_submit():
        user = User.create(form.email.data, form.password.data)
        return redirect(url_for('index'))
    else:
        flash(form.errors)
    return render_template('register.html', form=form)
