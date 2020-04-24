import sys
from pathlib import Path

project_dir = Path(__file__).resolve().parents[2]
sys.path.insert(0, project_dir)
import altair as alt
import numpy as np
import pandas as pd
import panel as pn
from bokeh.models import ColumnDataSource, LinearColorMapper, RedoTool, UndoTool, TapTool, LassoSelectTool, \
    BoxSelectTool, Image, Rect, WheelZoomTool, ResetTool, Tap, PanTool
from bokeh.plotting import figure
from bokeh.palettes import Colorblind8


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

gg_matrix = np.zeros((25, 25))
# gg_matrix[1:10, 1:37] = glider_gun
# gg_matrix = gg_matrix

args = pn.state.session_args
X = np.array(get_arg('X', args, gg_matrix))

N_y = X.shape[0]
N_x = X.shape[1]

n_steps = get_arg('n_steps', args, 1000)
X = X.astype(int)

# args = pn.state.curdoc.session_context.request.arguments
# print(f'Panel side {args}')

new_palette = ['#FFFFFF'] + list(Colorblind8)
new_palette_draw = ['palegoldenrod', 'indigo']
mapper = LinearColorMapper(palette=new_palette, low=0, high=4)
mapper_draw = LinearColorMapper(palette=new_palette_draw, low=0, high=1)
rev_mapper_draw = LinearColorMapper(palette=new_palette_draw[::-1], low=0, high=1)


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
    X_dict = {}
    for i in range(n_steps):
        X = life_step_2(X)
        r = np.random.randint(low=1, high=4, size=X.shape)
        col_X = X.astype(int).copy()
        col_X = r * col_X
        X_dict[i] = col_X
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


p = figure(tools=[])

# Create player figure
###################################
# ds = ColumnDataSource(data=to_df(X))
player = pn.widgets.DiscretePlayer(options=list(range(n_steps)), interval=10)
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
##################################

# Create drawing figure:
##################################
X_draw = np.random.binomial(1,0.001,size = X.shape)
source_draw = ColumnDataSource({'image': [X_draw]})
p_draw = figure(tools=[])
img_draw = p_draw.image(image='image', x=0, y=0, dw=X.shape[1], dh=X.shape[0], color_mapper=mapper_draw, level="image",
                        source=source_draw)
tools = [WheelZoomTool(), ResetTool(), PanTool()]

p_draw.add_tools(*tools)
p_draw.toolbar.active_drag = tools[2]
p_draw.toolbar.active_scroll = tools[0]


def tap_callback(event:Tap):
    x = np.ceil(event.x+0.5).astype(int)
    y = np.ceil(event.y+0.5).astype(int)
    new_data = np.array(source_draw.data['image'][0])
    print(x)
    print(y)
    new_data[y, x] = 1 if new_data[y, x] == 0 else 0
    print(new_data)

    source_draw.data = {'image': [new_data]}
     # use event['x'], event['y'], event['sx'], event['sy']


p_draw.on_event('tap', tap_callback)

pane = pn.Row(p_draw)
pane.servable()
