from flask import Flask, render_template, g, request, jsonify, send_file, redirect
import game
from flask_sqlalchemy import SQLAlchemy
import os
import json

from models import Board, History, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/postgres'
db = SQLAlchemy(app)



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
        user = request.form.get("user")
        board = request.form.get("board")

        new_board = Board(owner=user, board=board)
        db.session.add(new_board)
        db.session.commit()
        return redirect("/games", code=302)
        
    #get request returns the input page for a user to submit their eventual board TODO
    #post retrieves the actual board input and submits it into the game queue for eventual playing with others in the queue
    @app.route("/input", methods=["GET"])
    def input(boardSize=None):
        boardSize = 30

        return render_template('input.html', boardSize=boardSize)

    # eventual edit maybe TODO
    @app.route("/input/<int:board_id>")
    def edit_input(self):
        return

    @app.route("/users")
    def users():
        return render_template('users.html',users=User.query.all())

    @app.route("/boards")
    def boards():
        return render_template('boards.html', boards=Board.query.all())

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
    def test(self, boardSize=None):
        boardSize = 30
        if (request.method == "GET"):
            return render_template('tag.html', boardSize=boardSize)
        elif (request.method == "POST"):
            self.gameQueue.append(request.form['userBoard'])


# AG = Actual Generation, EG = Expected Generation,

#  sigma(EG) - (1/(AG-EG))


# runs servlet, debug=true if you want to test running code
if __name__ == "__main__":
    app.run(debug=True)
