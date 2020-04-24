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
    board_name = db.Column(db.String(128))
    board_elo = db.Column(db.Integer)
    board_owner = db.Column(db.Integer, db.ForeignKey('users.id'))
    board = db.Column(db.JSON)

    def __init__(self, owner, board):
        self.board_elo = 1500
        self.board_owner = owner
        self.board = board
        self.board_name = "test"

    def __repr__(self):
        return f"<Board {self.id} {self.board_elo} {self.board_owner} {self.board_name} {self.board}>"


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    #email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.id} {self.username}>"
