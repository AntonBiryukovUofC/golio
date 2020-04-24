import json

import altair as alt
import numpy as np
import pandas as pd
import panel as pn
import panel.widgets as pnw
import param
from bokeh.models import ColumnDataSource,LinearColorMapper
from bokeh.plotting import figure, curdoc
from bokeh.palettes import Colorblind8
import requests


def get_arg(key, args, default):
    str_val = args.get(key, None)
    if str_val is None:
        return default
    try:
        res = eval(str_val[0])

    except NameError:  # an actual string
        res = str_val[key][0]
    return res


pn.extension('vega')
glider_gun = \
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
     [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

gg_matrix = np.zeros((150, 170))
gg_matrix[1:10, 1:37] = glider_gun
gg_matrix = gg_matrix




args = pn.state.session_args
X = np.array(get_arg('X', args, gg_matrix))

N_y = X.shape[0]
N_x = X.shape[1]

n_steps = get_arg('n_steps', args, 1000)
X = X.astype(int)


# args = pn.state.curdoc.session_context.request.arguments
# print(f'Panel side {args}')




def chart(x):
    df = pd.DataFrame(data=x).stack().reset_index()
    df.columns = ['Y', 'X', 'val']
    ch = alt.Chart(data=df, width=600, height=600).encode(x='X:O', y='Y:O', fill='val:N').mark_rect()
    return ch


def to_df(x):
    df = pd.DataFrame(data=x).stack().reset_index()
    df.columns = ['Y', 'X', 'val']
    return df



def submit_data(_event):
    # get the data properly (as a numpy array?)
    board = [[0, 0, 0, 0, 0, ], [0, 0, 0, 0, 0, ], [0, 1, 1, 1, 0, ], [0, 0, 0, 0, 0, ], [0, 0, 0, 0, 0, ], ]

    data = {
        "board": board,
        "username": username.value,
        "boardname": boardname.value
    }
    json_data = json.dumps(data)

    print(json_data)
    requests.post("localhost:2342", data=json_data)


username = pn.widgets.TextInput(name='Username', value='Robert \'); DROP TABLE USERS;--')
boardname = pn.widgets.TextInput(name='Boardname', value='root')
submit_button = pn.widgets.Button(name='Submit', button_type='primary')
submit_button.on_click(submit_data)

pane = pn.Column(args, username, boardname, submit_button)
pane.servable()
