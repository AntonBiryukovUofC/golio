import mysql.connector as db
from flask import Flask, render_template, g, request, jsonify, send_file
import config
import game

app = Flask(__name__)

config = config.get()

# connect to db server

class Servlet:
    def __init__(self):
        self.gameQueue = []
        cnx = db.connect(**config['mysql']['config'])
        self.cursor = cnx.cursor()

    #default homepage, routed from home and the base url
    @app.route("/")
    def home():
        return render_template('landing.html')

    #get request returns the input page for a user to submit their eventual board
    #post retrieves the actual board input and submits it into the game queue for eventual playing with others in the queue
    @app.route("/input/<int:boardSize>", methods=["GET", "POST"])
    @app.route("/input", methods=["GET", "POST"])
    def input(boardSize=None):
        if(boardSize not in [5,10,20,30]):
            boardSize = 5
        print(boardSize)
        if(request.method == "GET"):
            return render_template('input.html',boardSize=boardSize)
        elif(request.method == "POST"):
            self.cursor.execute("insert into games {0}").format(request.form['userBoard'],request.form['userID'])

    #get request returns the input page for a user to submit their eventual board
    #post retrieves the actual board input and submits it into the game queue for eventual playing with others in the queue
    @app.route("/test/<int:boardSize>", methods=["GET", "POST"])
    @app.route("/test", methods=["GET", "POST"])
    def test(boardSize=None):
        if(boardSize not in [5,10,20,30]):
            boardSize = 5
        print(boardSize)
        if(request.method == "GET"):
            return render_template('tag.html',boardSize=boardSize)
        elif(request.method == "POST"):
            self.gameQueue.append(request.form['userBoard'])


#  query = "SELECT altitude, {0} FROM flight_data WHERE flight_number = {1}".format(column, flight_number)
#  cursor.execute(query)
#  rows = cursor.fetchall()

#AG = Actual Generation, EG = Expected Generation,

#  sigma(EG) - (1/(AG-EG))




#runs servlet, debug=true if you want to test running code
if __name__ == "__main__":
    app.run(debug=True)
