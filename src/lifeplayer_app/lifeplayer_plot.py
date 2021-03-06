import altair as alt
import numpy as np
import pandas as pd
import panel as pn
from bokeh.models import ColumnDataSource, LinearColorMapper, ColorBar, CategoricalColorMapper, FixedTicker, Div
from bokeh.palettes import Colorblind8
from bokeh.plotting import figure
import sys

sys.path.insert(0, '/home/anton/Repos/golio')
from src.common.gamestate import GameState


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
gg_matrix = np.random.randint(0, 5, size=gg_matrix.shape)

args = pn.state.session_args
X = np.array(get_arg('X', args, gg_matrix))

N_y = X.shape[0]
N_x = X.shape[1]

usernames = get_arg('usernames', args, ['a', 'b'])
n_steps = get_arg('n_steps', args, 50)
X = X.astype(int)

# args = pn.state.curdoc.session_context.request.arguments
# print(f'Panel side {args}')

new_palette = ['#FFFFFF'] + list(Colorblind8)[0:len(usernames)]
mapper = LinearColorMapper(palette=new_palette, low=0, high=len(usernames))
ticks = ["Dead"] + usernames
label_dict = {i: ticks[i] for i in range(len(ticks))}
mapper_cb = CategoricalColorMapper(palette=new_palette[0:len(usernames) + 1], factors=["Dead"] + usernames)

div = pn.Row(*[
    pn.pane.Markdown(f'# {ticks[i]}', style={'color': new_palette[i]}) for i in range(len(ticks))
])


def life_step_1(X):
    """Game of life step using generator expressions"""
    nbrs_count = sum(np.roll(np.roll(X, i, 0), j, 1)
                     for i in (-1, 0, 1) for j in (-1, 0, 1)
                     if (i != 0 or j != 0))
    return (nbrs_count == 3) | (X & (nbrs_count == 2))


def life_step_2(X):
    """Game of life step using scipy tools"""
    from scipy.signal import convolve2d
    nbrs_count = convolve2d(X, np.ones((3, 3)), mode='same', boundary='wrap') - X
    return (nbrs_count == 3) | (X & (nbrs_count == 2))


def life_do_steps(X, n_steps):
    print('Calculating all steps....')
    gs = GameState.from_numpy_array(X)
    X_dict = {}
    for i in range(n_steps):
        gs = gs.step()
        X = gs.get_numpy_array()
        X_dict[i] = X
    return X_dict


def chart(x):
    df = pd.DataFrame(data=x).stack().reset_index()
    df.columns = ['Y', 'X', 'val']
    ch = alt.Chart(data=df, width=600, height=600).encode(x='X:O', y='Y:O', fill='val:N').mark_rect()
    return ch


def to_df(x):
    df = pd.DataFrame(data=x).stack().reset_index()
    df.columns = ['Y', 'X', 'val']
    return df


# chart_alt = pn.pane.Pane(chart(x=np.random.randint(low=0, high=12, size=(N_y, N_x))))


p = figure(tools=[], width=900, height=800)
# ds = ColumnDataSource(data=to_df(X))
player = pn.widgets.DiscretePlayer(options=list(range(n_steps)), interval=60)
X_dict = life_do_steps(X, n_steps=n_steps + 1)
source = ColumnDataSource({'image': [X]})
img = p.image(image='image', x=0, y=0, dw=10, dh=10, color_mapper=mapper, level="image",
              source=source)
p.xaxis.visible = False
p.xgrid.visible = False
p.yaxis.visible = False
p.ygrid.visible = False


def reset_chart(target, event):
    m = X_dict[event.new]
    source.data = {'image': [m]}


player.link(img, callbacks={'value': reset_chart})
player.value = 0
pane = pn.Column(div, player, p)
pane.servable()
