import numpy as np
import pandas as pd
from bokeh.layouts import column, row, gridplot, widgetbox, layout
from bokeh.models import Button, HoverTool
from bokeh.palettes import RdYlBu3
import bokeh.plotting as bp
from bokeh.charts import Histogram
from bokeh.tile_providers import WMTSTileSource
from bokeh.models.sources import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput, Select, RangeSlider
from bokeh.io import output_file, show
import data_tools as dtools
import plotting_tools as ptools

map_x_range, map_y_range = (13884029,12553304), (-2698291,6455972)

df_fushimi = dtools.read_prepare_data("Fushimi")
df_diamond = dtools.read_prepare_data("Diamond")
df = df_diamond

##Initialize the figures and data source
source = ColumnDataSource(
    data = {
        'long1': [],
        'lat1': [],
        'wmlong1': [],
        'wmlat1': [],
        'timestamp1': [],
        'timestamp_date': [],
        'feature_ts': [],
        'feature_ts2': [],
        'x': [],
        'y': [],
    }
)

fig_map = ptools.draw_map(map_x_range, map_y_range)
fig_ts = ptools.draw_timeseries(y_label='feature_ts')
fig_ts2 = ptools.draw_timeseries(y_label='feature_ts2')
fig_plot = ptools.draw_plot(x_label='X', y_label='Y')

fig_map.line('wmlong1', 'wmlat1',
             source=source, line_color='red', line_alpha=0.5, line_width=3)
fig_ts.line('timestamp1', 'feature_ts',
            source=source, line_color='navy', line_alpha=0.5, line_width=3)
fig_ts2.line('timestamp1', 'feature_ts2',
            source=source, line_color='navy', line_alpha=0.5, line_width=3)
fig_plot.circle('x', 'y',
                source=source, fill_color='navy', line_color=None, alpha=0.3, size=5)

##Set up widgets
ww = 300
wh = int(800/7)
ship_selector = Select(title="Ship name (use with caution!)", value="Diamond",
                       options=["Diamond", "Fushimi"], width=ww) ##FIXME! Error handling for columns that only exist in one df but not the other needed!!
feature_ts_selector = Select(title="Feature_ts:", value="12",
                             options=list(df.loc[:,df.dtypes == 'float64'].columns), width=ww)
feature_ts2_selector = Select(title="Feature_ts2:", value="12",
                              options=list(df.loc[:,df.dtypes == 'float64'].columns), width=ww)
x_selector = Select(title="X:", value="12",
                    options=list(df.loc[:,df.dtypes == 'float64'].columns), width=ww)
y_selector = Select(title="Y:", value="wmlat2",
                    options=list(df.loc[:,df.dtypes == 'float64'].columns), width=ww)
from_slider = Slider(title="from step", value=0, start=0, end=len(df), step=1, width=ww)
to_slider = Slider(title="to step", value=100, start=0, end=len(df), step=1, width=ww)

#range_slider = RangeSlider(title='index range', start=0, end=len(df), range=(10,100), step=10, width=ww)

##Update the data based on inputs
# def update_plot_labels(attrname, old, new):
#     fig_ts.yaxis.axis_label = to_slider.value
#     to_slider.on_change('value', update_plot_labels)
    
def update_data(attrname, old, new):
    global df
    if str(new).lower() == 'fushimi':
        df = df_fushimi
    elif str(new).lower() == 'diamond':
        df = df_diamond
        
    # Get the current slider values
    from_ind = from_slider.value
    to_ind = to_slider.value
    # from_ind = range_slider.range[0]
    # to_ind = range_slider.range[1]
    feature_ts_select = feature_ts_selector.value
    feature_ts2_select = feature_ts2_selector.value
    x_select = x_selector.value
    y_select = y_selector.value
    
    # Generate the new curve
    long1 = df['long1'][from_ind:to_ind]
    lat1 = df['lat1'][from_ind:to_ind]
    wmlong1 = df['wmlong1'][from_ind:to_ind]
    wmlat1 = df['wmlat1'][from_ind:to_ind]
    timestamp1 = df['timestamp1'][from_ind:to_ind]
    timestamp_date = df['timestamp_date'][from_ind:to_ind]
    feature_ts = df[feature_ts_select][from_ind:to_ind]
    feature_ts2 = df[feature_ts2_select][from_ind:to_ind]
    x = df[x_select][from_ind:to_ind]
    y = df[y_select][from_ind:to_ind]

    source.data = dict(
        long1=long1, lat1=lat1,
        wmlong1=wmlong1, wmlat1=wmlat1,        
        timestamp1=timestamp1,
        feature_ts=feature_ts,
        feature_ts2=feature_ts2,
        x=x, y=y,
        timestamp_date=timestamp_date,
    )
        
for w in [
        ship_selector,
        from_slider,
        to_slider,
        feature_ts_selector,
        feature_ts2_selector,
        x_selector,
        y_selector,
]:
    w.on_change('value', update_data)
#    range_slider.on_change('range', update_data)
    
##Organize the layout
widgets = column(
    children=[
        ship_selector,
        feature_ts_selector,
        feature_ts2_selector,
        x_selector,
        y_selector,
#        range_slider
        from_slider,
        to_slider
    ],
    sizing_mode="fixed"
)
first_row = row(fig_map, fig_plot)
plots = column(first_row, fig_ts, fig_ts2)

bp.curdoc().add_root(row(widgets, plots))
bp.curdoc().title = 'ShipDash'
