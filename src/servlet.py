from flask import Flask, render_template, g, request, jsonify, send_file, redirect
import game
from flask_sqlalchemy import SQLAlchemy
import os
import json

from models import Board, History, User, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mysecretpassword@localhost/postgres'
db.init_app(app)
app.app_context().push()
db.create_all()
db.session.commit()


# connect to db server

class Servlet:
    def __init__(self):
        self.gameQueue = []

    # default homepage, routed from home and the base url
    @app.route("/")
    def home():
        return render_template('landing.html')


    #store into db
    @app.route("/submit_board", methods=["POST"])
    def submit_board():
        data = request.json

        if User.query.filter(User.username==data["user"]).first() is None:
            new_user = User(username=data["user"])
            db.session.add(new_user)
            db.session.commit()
            user_id = new_user.id
        else:
            user_id = User.query.filter(User.username==data["user"]).first().id

        new_board = Board(owner=user_id, board=data["board"])
        db.session.add(new_board)
        db.session.commit()
        return 'success', 200
        
    #get request returns the input page for a user to submit their eventual board TODO
    #post retrieves the actual board input and submits it into the game queue for eventual playing with others in the queue
    @app.route("/input", methods=["GET"])
    def input(boardSize=None):
        boardSize = 25

        return render_template('input.html', boardSize=boardSize)

    @app.route("/playmatch", methods=["POST"])
    def playmatch():
        print(request.data)
        return redirect("/history")

    # eventual edit maybe TODO
    @app.route("/input/<int:board_id>")
    def edit_input(self):
        return

    @app.route("/users")
    def users():
        return render_template('users.html',users=User.query.all())

    @app.route("/boards")
    def boards():
        args = request.args
        username = args.get("username", None)
        if username is None:
            return render_template('boards.html', otherboards=Board.query.all(), username=None)
        else:
            user_id = User.query.filter(User.username==username).first().id
            return render_template('boards.html', userboards=Board.query.filter(Board.board_owner==user_id),
                                   otherboards=Board.query.filter(Board.board_owner != user_id), username=username)

    #list all results from db query TODO
    @app.route("/games", methods=["GET"])
    def history():
        return render_template('games.html',users=History.query.all())

    # visualize a game TODO
    @app.route("/results/<int:game_id>")
    def game(self):
        return

    # get request returns the input page for a user to submit their eventual board TODO
    # post retrieves the actual board input and submits it into the game queue for eventual playing with others in the queue
    @app.route("/test/<int:boardSize>", methods=["GET", "POST"])
    @app.route("/test", methods=["GET", "POST"])
    def test(self,boardSize=None):
        boardSize = 25
        if(request.method == "GET"):
            return render_template('tag.html',boardSize=boardSize)
        elif(request.method == "POST"):
            self.gameQueue.append(request.form['userBoard'])


# AG = Actual Generation, EG = Expected Generation,

#  sigma(EG) - (1/(AG-EG))


# runs servlet, debug=true if you want to test running code
if __name__ == "__main__":
    app.run(debug=True)
