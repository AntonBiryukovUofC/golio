db schema

Table Name:
games

Column Name, Type:
boardID         int                 pkey
username        varchar 50          
subBoardSize    int
boardSize       int 
boardRank       int
EG              double

________________________________________________________________________________

Table Name:
users

Column Name, Type:
userID          int                 pkey
username        varchar 50          index
hashedPass      varchar 100 ?
boardList       JSON TODO decide?

________________________________________________________________________________

Table Name:
history

Column Name, Type:
matchID         int                 pkey
boardSize       int
subBoardSize    int
boardList       JSON      (boardID, EG, AG)

________________________________________________________________________________
