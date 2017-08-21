import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from bokeh.layouts import column, row, gridplot, widgetbox, layout
from bokeh.models import Button, HoverTool
import bokeh.plotting as bp
from bokeh.tile_providers import WMTSTileSource
from bokeh.models.sources import ColumnDataSource
from bokeh.models.widgets import Slider

##Global settings
#FIXME! figure settings!
TOOLS="pan,wheel_zoom,box_zoom,reset"

map_width = 400
map_height = map_width

scatter_width = map_width
scatter_height = scatter_width

ts_width = map_width*2
ts_height = map_height/2

def datetime(x):
        return np.array(x, dtype=np.datetime64)

def make_colormap(df, col):
    argsortcol = np.argsort(df[col])
    colors = ["#%02x%02x%02x" % (int(r), int(g), int(b)) for r, g, b, _ in 255*mpl.cm.viridis(mpl.colors.Normalize()(argsortcol))]
    return colors
    
def draw_map(x_range, y_range):
    fig = bp.figure(
        tools = TOOLS,
        x_range = x_range,
        y_range = y_range,
        plot_width = map_width,
        plot_height = map_height,
        outline_line_color = None,        
    )
    hover = HoverTool(
        tooltips=[
            ('date', '@timestamp_date'),
            ('longitude', '@long1'),
            ('lattitude', '@lat1'),
        ]
    )
    fig.add_tools(hover)
    fig.toolbar.logo = None
    fig.xgrid.grid_line_color = None
    fig.ygrid.grid_line_color = None
    fig.axis.visible = False
    url = 'http://c.tile.openstreetmap.org/{Z}/{X}/{Y}.png'
    attribution = ""#Map tiles by Carto, under CC BY 3.0. Data by OpenStreetMap, under ODbL"
    fig.add_tile(WMTSTileSource(url=url, attribution=attribution))
    return fig

def draw_timeseries(y_label):
    fig = bp.figure(
        tools = TOOLS,
        x_axis_type = "datetime",
        plot_width = ts_width,
        plot_height = ts_height,
        x_axis_label = 'date/time',
        y_axis_label = y_label,
        outline_line_color = None,
    )
    hover = HoverTool(
        tooltips=[
            ('date', '@timestamp_date'),
            ('longitude', '@long1'),
            ('lattitude', '@lat1'),
        ]
    )
    fig.add_tools(hover)
    fig.toolbar.logo = None
    fig.xgrid.grid_line_color = None
    fig.ygrid.grid_line_color = None
    return fig

def draw_plot(x_label, y_label):
    fig = bp.figure(
        tools = TOOLS,
        plot_width = scatter_width,
        plot_height = scatter_height,
        x_axis_label = x_label,
        y_axis_label = y_label,
        outline_line_color = None,        
    )
    hover = HoverTool(
        tooltips=[
            ('date', '@timestamp_date'),
            ('longitude', '@long1'),
            ('lattitude', '@lat1'),
        ]
    )
    fig.add_tools(hover)
    fig.toolbar.logo = None
    fig.xgrid.grid_line_color = None
    fig.ygrid.grid_line_color = None
    return fig

