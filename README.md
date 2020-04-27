# Multiplayer Game of Life

This modification of the Game of Life (GoL) was born in the honor of recently passed away John Conway, as well as the main topic of 2 day ETB Hackathon.
The rules were adopted from the original GoL, with an additional twist that made the game competitive - the cells now need to have an owner.

# Main goals

Essentially, there are two main goals a player needs to prioritize over in order to win the match of GoL:

- Devise a way to expand into the space provided as widely as possible
- Stay alive for the longest period of time (generations)

# Technology stack

The implementation is a Frankenstein relying on several packages/programming languages:

- JS / Jinja templates for the front-end (web-app) and single-player visualization
- Python with Flask + SQLAlchemy for the backend
- Bokeh for the multiplayer visualization

# How to run

Provided all the requirements are satisfied:

- `python src/servlet.py`
- hit the `localhost/generate` endpoint to generate opponents with random starting configurations
- go to `Input` tab, create your board, submit
- go to `Boards` tab, and select who you'd like to play against
- hit `Play match`
- go to Games tab to find out who won & watch the game animation



### Appendix

I think the info below might be outdated...

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



  pg_ctl -D /usr/local/var/postgres start