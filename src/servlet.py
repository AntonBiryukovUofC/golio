from flask import Flask, render_template, g, request, jsonify, send_file
import game
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)


db = SQLAlchemy(app)


# connect to db server

class Servlet:
    def __init__(self):
        self.gameQueue = []

    #default homepage, routed from home and the base url
    @app.route("/")
    def home():
        return render_template('landing.html')

    #store into db TODO
    @app.route("/submit_board")
    def submit_board():
        self.cursor.execute("insert into games {0}").format(request.form['userBoard'],request.form['userID'])
        return
        
    #get request returns the input page for a user to submit their eventual board TODO
    #post retrieves the actual board input and submits it into the game queue for eventual playing with others in the queue
    @app.route("/input", methods=["GET"])
    def input(boardSize=None):
        boardSize = 30

        return render_template('input.html',boardSize=boardSize)

    #eventual edit maybe TODO
    @app.route("/input/<int:board_id>")
        return

    #list all results from db query TODO
    @app.route("/results", methods=["GET"])
        return

    #visualize a game TODO
    @app.route("/results/<int:game_id>")
        return

    #get request returns the input page for a user to submit their eventual board TODO
    #post retrieves the actual board input and submits it into the game queue for eventual playing with others in the queue
    @app.route("/test/<int:boardSize>", methods=["GET", "POST"])
    @app.route("/test", methods=["GET", "POST"])
    def test(boardSize=None):
        boardSize = 30
        if(request.method == "GET"):
            return render_template('tag.html',boardSize=boardSize)
        elif(request.method == "POST"):
            self.gameQueue.append(request.form['userBoard'])


#AG = Actual Generation, EG = Expected Generation,

#  sigma(EG) - (1/(AG-EG))




#runs servlet, debug=true if you want to test running code
if __name__ == "__main__":
    app.run(debug=True)
