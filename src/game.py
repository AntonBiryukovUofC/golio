import mysql.connector as db
import config

config = config.get()

class Game:

    def __init__():
        self.playerInputs = {"player1":[],"player2":[],"player3":[],"player4":[]}
        self.generation = 0 #move number
        self.inputSize = 0
        self.boardSize = 100
        self.liveCells = 0


    #game logic for determining which of the cells neighbors are live and dead, implements toroidal array for board
    #first creates a list of parent cells, then adds the live cells surrounding the cell, finally adds the colours of parents(user ids)
    def checkNeighbors(gameboard, cell, boardHeight):
        aliveCells = 0
        parent_list = []
        parent_colours = []
        # game board is a toroid
        if(cell[0] == 0 and cell[1] == 0):#top left
            parent_list = [gameboard[boardHeight][boardHeight],  gameboard[boardHeight][0],  gameboard[boardHeight][1],  gameboard[0][boardHeight],  gameboard[cell[0]][cell[1]+1],  gameboard[1][boardHeight],  gameboard[cell[0]+1][cell[1]],  gameboard[cell[0]+1][cell[1]+1]]
        elif(cell[0] == 0 and cell[1] == boardHeight):#top right
            parent_list = [gameboard[boardHeight][cell[1]-1],  gameboard[boardHeight][cell[1]],  gameboard[boardHeight][0],  gameboard[cell[0]][cell[1]-1],  gameboard[cell[0]][0],  gameboard[cell[0]+1][cell[1]-1],  gameboard[cell[0]+1][cell[1]],  gameboard[cell[0]+1][0]]
        elif(cell[0] == boardHeight and cell[1] == 0):#bottom left
            parent_list = [gameboard[cell[0]-1][boardHeight],  gameboard[cell[0]-1][cell[1]],  gameboard[cell[0]-1][cell[1]+1],  gameboard[cell[0]][boardHeight],  gameboard[cell[0]][cell[1]+1],  gameboard[0][boardHeight],  gameboard[0][cell[1]],  gameboard[0][cell[1]+1]]
        elif(cell[0] == boardHeight and cell[1] == boardHeight):#bottom right
            parent_list = [gameboard[cell[0]-1][cell[1]-1],  gameboard[cell[0]-1][cell[1]],  gameboard[cell[0]-1][boardHeight],  gameboard[cell[0]][cell[1]-1],  gameboard[cell[0]][0],  gameboard[0][cell[1]-1],  gameboard[0][cell[1]],  gameboard[0][0]]
        elif(cell[0] == 0 and cell[1] != boardHeight):#top
            parent_list = [gameboard[boardHeight][cell[1]-1],  gameboard[boardHeight][cell[1]],  gameboard[boardHeight][cell[1]+1],  gameboard[cell[0]][cell[1]-1],  gameboard[cell[0]][cell[1]+1],  gameboard[cell[0]+1][cell[1]-1],  gameboard[cell[0]+1][cell[1]],  gameboard[cell[0]+1][cell[1]+1]]
        elif(cell[1] == 0 and cell[0] != boardHeight):#left
            parent_list = [gameboard[cell[0]-1][boardHeight],  gameboard[cell[0]-1][cell[1]],  gameboard[cell[0]-1][cell[1]+1],  gameboard[cell[0]][boardHeight],  gameboard[cell[0]][cell[1]+1],  gameboard[cell[0]+1][boardHeight],  gameboard[cell[0]+1][cell[1]],  gameboard[cell[0]+1][cell[1]+1]]
        elif(cell[1] == boardHeight):#right
            parent_list = [gameboard[cell[0]-1][cell[1]-1],  gameboard[cell[0]-1][cell[1]],  gameboard[cell[0]-1][0],  gameboard[cell[0]][cell[1]-1],  gameboard[cell[0]][0],  gameboard[cell[0]+1][cell[1]-1],  gameboard[cell[0]+1][cell[1]],  gameboard[cell[0]+1][0]]
        elif(cell[0] == boardHeight):#bottom
            parent_list = [gameboard[cell[0]-1][cell[1]-1],  gameboard[cell[0]-1][cell[1]],  gameboard[cell[0]-1][cell[1]+1],  gameboard[cell[0]][cell[1]-1],  gameboard[cell[0]][cell[1]+1],  gameboard[0][cell[1]-1],  gameboard[0][cell[1]],  gameboard[0][cell[1]+1]]
        else:#everything else
            parent_list = [gameboard[cell[0]-1][cell[1]-1],  gameboard[cell[0]-1][cell[1]],  gameboard[cell[0]-1][cell[1]+1],  gameboard[cell[0]][cell[1]-1],  gameboard[cell[0]][cell[1]+1],  gameboard[cell[0]+1][cell[1]-1],  gameboard[cell[0]+1][cell[1]],  gameboard[cell[0]+1][cell[1]+1]]

        for i in parent_list:
            aliveCells += i[0]
            if(i[1] not in parent_colours):
                parent_colours.append(i[1])

        self.liveCells = aliveCells
        return [aliveCells, parent_colours]

    def insertBoard(gameboard,subboard,startCell):
        for i in range(0,subboard.length):
            for j in range(0,subboard.length):
                gameboard[startCell[0]+i][startCell[1]+j] = subboard[i][j]
