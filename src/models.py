from sqlalchemy.dialects.postgresql import JSON
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class History(db.Model):
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True)
    boards_included = db.Column(db.ARRAY(db.Integer))
    winner = db.Column(db.Integer)

    def __init__(self, boards_included):
        self.url = url
        self.boards_included = boards_included

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Board(db.Model):
    __tablename__ = 'boards'

    id = db.Column(db.Integer, primary_key=True)
    board_elo = db.Column(db.Integer)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Board {self.id}>'

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User {self.user}>'.format(self.username)
