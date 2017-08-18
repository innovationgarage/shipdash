import numpy as np
import pandas as pd
from bokeh.layouts import column, row, gridplot, widgetbox, layout
from bokeh.models import Button, HoverTool
from bokeh.palettes import RdYlBu3
import bokeh.plotting as bp
from bokeh.tile_providers import WMTSTileSource
from bokeh.models.sources import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput, Select
from bokeh.io import output_file, show
import data_tools as dtools
import plotting_tools as ptools
map_x_range, map_y_range = (13884029,12553304), (-2698291,6455972)

##Initialize the figures and data source
df = dtools.read_prepare_data('Fushimi')
#source = ColumnDataSource.from_df(df)

source = ColumnDataSource(
    data = {
        'long1': [],
        'lat1': [],
        'timestamp1': [],
        'feature1': [],
        'feature2': [],
        'feature3': []
    }
)

fig_map = ptools.make_new_fig('map', map_x_range, map_y_range)
fig_ts1 = ptools.make_new_fig('time_series')
fig_ts2 = ptools.make_new_fig('time_series')
fig_ts3 = ptools.make_new_fig('time_series')

fig_map.line('long1', 'lat1',
             source=source, line_color='red', line_alpha=0.5, line_width=3)
fig_ts1.line('timestamp1', 'feature1',
             source=source, line_color='black', line_alpha=0.5, line_width=3)
fig_ts2.line('timestamp1', 'feature2',
             source=source, line_color='blue', line_alpha=0.5, line_width=3)
fig_ts3.line('timestamp1', 'feature3',
             source=source, line_color='cyan', line_alpha=0.5, line_width=3)

##Set up widgets
from_slider = Slider(title="from step", value=0, start=0, end=len(df), step=10)
to_slider = Slider(title="to step", value=100, start=0, end=len(df), step=10)

# feature_selector1 = TextInput(title="feature1", value='12')
# feature_selector2 = TextInput(title="feature2", value='14')
# feature_selector3 = TextInput(title="feature3", value='18')

feature_selector1 = Select(title="Feature1:", value="12",
                           options=list(df.loc[:,df.dtypes == 'float64'].columns))
feature_selector2 = Select(title="Feature2:", value="14",
                           options=list(df.loc[:,df.dtypes == 'float64'].columns))
feature_selector3 = Select(title="Feature3:", value="18",
                           options=list(df.loc[:,df.dtypes == 'float64'].columns))

##Update the data based on inputs
def update_title(attrname, old, new):
    plot.title.feature_selector1 = feature_selector1.value
    feature_selector1.on_change('value', update_title)
    plot.title.feature_selector2 = feature_selector2.value
    feature_selector2.on_change('value', update_title)
    plot.title.feature_selector3 = feature_selector3.value
    feature_selector3.on_change('value', update_title)

def update_data(attrname, old, new):
    # Get the current slider values
    from_ind = from_slider.value
    to_ind = to_slider.value
    feature_select1 = feature_selector1.value
    feature_select2 = feature_selector2.value
    feature_select3 = feature_selector3.value    
    
    # Generate the new curve
    long1 = df['long1'][from_ind:to_ind]
    lat1 = df['lat1'][from_ind:to_ind]
    timestamp1 = df['timestamp1'][from_ind:to_ind]
    feature1 = df[feature_select1][from_ind:to_ind]
    feature2 = df[feature_select2][from_ind:to_ind]
    feature3 = df[feature_select3][from_ind:to_ind]    
    source.data = dict(long1=long1, lat1=lat1,
                       timestamp1=timestamp1,
                       feature1=feature1,
                       feature2=feature2,
                       feature3=feature3)
        
for w in [from_slider, to_slider, feature_selector1, feature_selector2, feature_selector3]:
    w.on_change('value', update_data)
    
##Organize the layout
inputs = widgetbox(feature_selector1,
                   feature_selector2,
                   feature_selector3,
                   from_slider, to_slider)
grid = gridplot(
    [fig_map, fig_ts1, fig_ts2, fig_ts3],
    ncols = 2,
    merge_tools=True, toolbar_location='right')

bp.curdoc().add_root(row(inputs, grid))
bp.curdoc().title = 'ShipDash'
