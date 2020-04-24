from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class History(db.Model):
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True)
    boards_included = db.Column(db.ARRAY(db.Integer))
    winner = db.Column(db.String(128), db.ForeignKey('users.username'))

    def __init__(self, boards_included, winner):
        self.boards_included = boards_included
        self.winner = winner

    def __repr__(self):
        return f"<id {self.id}>"


class Board(db.Model):
    __tablename__ = 'boards'

    id = db.Column(db.Integer, primary_key=True)
    board_name = db.Column(db.String(128))
    board_elo = db.Column(db.Integer)
    board_owner = db.Column(db.String(128), db.ForeignKey('users.username'))
    board = db.Column(db.JSON)

    def __init__(self, owner, board):
        self.board_elo = 1500
        self.board_owner = owner
        self.board = board
        self.board_name = "test"

    def __repr__(self):
        return {"id":{self.id},"board_elo": {self.board_elo},"board_owner": {self.board_owner},"board_name": {self.board_name},"board": {self.board}}

    def __str__(self):
        return f"<Board {self.id} {self.board_elo} {self.board_owner} {self.board_name} {self.board}>"


class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    #email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"
