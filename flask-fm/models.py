# -*- coding: utf-8 -*-

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    playlist_id = db.Column(db.Integer,  db.ForeignKey('playlist.id'))

    def __repr__(self):
        return "{}".format(self.username)


class Song(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    artist = db.Column(db.String, unique=False, index=True)
    title = db.Column(db.String, unique=False, index=True)
    n = db.Column(db.Integer, index=False, unique=False)

    def __init__(self, title, artist, n=0, id=None):
        self.id = id
        self.title = title
        self.artist = artist
        self.n = n

    def increase_count(self):
        self.n += 1

    def __repr__(self):
        return "{} by {}".format(self.title, self.artist)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey(
        'song.id', ondelete="CASCADE"))
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'))

    def __repr__(self):
        return "{}".format(Song.query.get(self.song_id))


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    items = db.relationship('Item', backref='playlist', lazy='dynamic')

    def __repr__(self):
        return "Playlist {}".format(self.id)
