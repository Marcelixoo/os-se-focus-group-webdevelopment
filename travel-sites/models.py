from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(120), unique=True, index=True)
  email = db.Column(db.String(120), unique=True, index=True)
  posts = db.relationship('Post', backref='author', lazy='dynamic')

  def create(username, email, password):
    new_user = User(
      username=username,
      email=email
    )
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

  def set_password(self, password):
    self.password = generate_password_hash(password)

  def check_password_hash(self, password_to_check):
    return check_password_hash(self.password, password_to_check)

  def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(140))
    country = db.Column(db.String(140))
    description = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.description)