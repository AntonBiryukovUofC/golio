from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class History(db.Model):
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True)
    boards_included = db.Column(db.ARRAY(db.Integer))
    winner = db.Column(db.Integer)

    def __init__(self, boards_included):
        self.boards_included = boards_included

    def __repr__(self):
        return f"<id {self.id}>"


class Board(db.Model):
    __tablename__ = 'boards'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    board_elo = db.Column(db.Integer)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    board = db.Column(db.JSON)
    width = db.Column(db.Integer)

    def __init__(self, owner):
        self.board_elo = 1500
        self.owner = owner

    def __repr__(self):
        return f"<Board {self.id} {self.board_elo} {self.owner}>"


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.id} {self.username} {self.email}>"
