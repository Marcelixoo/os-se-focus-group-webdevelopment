# -*- coding: utf-8 -*-

from flask import render_template, request, url_for, redirect, flash

from app import app, db
from models import User, Song, Playlist, Item
from forms import SongForm


def exists(item, playlist):
    """Return a boolean
      True if playlist contains item. False otherwise.
      """
    for i in playlist:
        if i.song_id == item.song_id:
            return True
    return False


@app.route('/profiles')
def profiles():
    current_users = User.query.all()
    return render_template('users.html', current_users=current_users)


@app.route('/profile/<int:user_id>')
def profile(user_id):
    user = (
        User
        .query
        .filter_by(id=user_id)
        .first_or_404(description="No such user found.")
    )
    songs = Song.query.all()
    my_playlist = (
        Playlist
        .query
        .filter_by(id=user.playlist_id)
        .one())
    return render_template('profile.html', user=user, songs=songs, my_playlist=my_playlist)


@app.route('/add_item/<int:user_id>/<int:song_id>/<int:playlist_id>')
def add_item(user_id, song_id, playlist_id):
    new_item = Item(song_id=song_id, playlist_id=playlist_id)
    user = (
        User.query
        .filter_by(id=user_id)
        .first_or_404(description="No such user found.")
    )
    my_playlist = (
        Playlist.query
        .filter_by(id=user.playlist_id)
        .first()
    )
    if not exists(new_item, my_playlist.items):
        song = Song.query.get(song_id)
        song.increase_count()
        db.session.add(new_item)
        db.session.commit()
    return redirect(url_for('profile', user_id=user_id))


@app.route('/remove_item/<int:user_id>/<int:item_id>')
def remove_item(user_id, item_id):
    item_to_remove = Item.query.get(item_id)
    db.session.delete(item_to_remove)
    db.session.commit()
    return redirect(url_for('profile', user_id=user_id))


@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    form = SongForm(csrf_enabled=False)
    if request.method == 'POST' and form.validate():
        new_song = Song(
            title=form.title.data,
            artist=form.artist.data,
        )
        new_song.increase_count()
        db.session.add(new_song)
        db.session.commit()
    elif form.errors:
        flash(form.errors)
    return render_template(
        'dashboard.html',
        songs=Song.query.all(),
        unpopular_songs=Song.query.order_by(Song.n).all(),
        form=form)
