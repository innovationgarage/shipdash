import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

from bokeh.layouts import column, row, gridplot, widgetbox, layout
from bokeh.models import Button, HoverTool
from bokeh.palettes import RdYlBu3
import bokeh.plotting as bp
from bokeh.tile_providers import WMTSTileSource
from bokeh.models.sources import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.io import output_file, show

def make_colormap(df, col):
    argsortcol = np.argsort(df[col])
    colors = ["#%02x%02x%02x" % (int(r), int(g), int(b)) for r, g, b, _ in 255*mpl.cm.viridis(mpl.colors.Normalize()(argsortcol))]
    return colors
    
def make_new_fig(fig_type, *args):
    pw = 400
    ph = 200
    TOOLS="resize,pan,wheel_zoom,box_zoom,reset,hover"
    if fig_type == 'map':
#        x_range,y_range = ((13884029,12553304), (-2698291,6455972))
        fig = bp.figure(
            tools = TOOLS,
            x_range = args[0],
            y_range = args[1],
            plot_width = pw,
            plot_height = ph
        )
        url = 'http://c.tile.openstreetmap.org/{Z}/{X}/{Y}.png'
        attribution = ""#Map tiles by Carto, under CC BY 3.0. Data by OpenStreetMap, under ODbL"
        fig.add_tile(WMTSTileSource(url=url, attribution=attribution))
    elif fig_type == 'time_series':
        fig = bp.figure(
            tools = TOOLS,
            x_axis_type = "datetime",
            plot_width = pw,
            plot_height = ph,
            x_axis_label = 'date/time'
        )
    return fig

