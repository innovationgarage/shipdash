import numpy as np
import pandas as pd
import matplotlib as mpl
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import Imputer

def clean(df, name):
    """Finds all empty space or all NaN columns and drops them from the DataFrame"""
    df.replace(r'\s+', np.nan, regex=True, inplace=True)
    df.replace(r'-', np.nan, regex=True, inplace=True)
    df.dropna(axis=1, how='all', inplace=True)
    df.columns = [str(x) for x in df.columns]
    df.reset_index(level=[0], inplace=True)
    df.rename(columns={'index': 'ind'}, inplace=True)
    ##FIXME! This is to find coordinate columns etc. manually, because we don't know anything about the structure of our data!
    df.to_csv(name+'_clean.csv')
    return df

def scale_impute(df, method):
    """Finds float columns, impute their NaN values with 'method', and then min-max scale the column/feature"""
    fill_NaN = Imputer(missing_values=np.nan, strategy=method, axis=1)
    df[df.loc[:, df.dtypes == 'float64'].columns.difference(['lat1', 'long1', 'lat2', 'long2'])] = fill_NaN.fit_transform(
        df[df.loc[:, df.dtypes == 'float64'].columns.difference(['lat1', 'long1', 'lat2', 'long2'])]
    )    
    scaler = MinMaxScaler()
    df[df.loc[:, df.dtypes == 'float64'].columns.difference(['lat1', 'long1', 'lat2', 'long2'])] = scaler.fit_transform(
        df[df.loc[:, df.dtypes == 'float64'].columns.difference(['lat1', 'long1', 'lat2', 'long2'])]
    )
    return df
                
def convert_coordinate(df, col_in, col_out):
    """Converts coordinates of the format [d]ddmm.mmm to [dd]d.ddd"""
    ##FIXME! This is assuming all coordinates are E and N 
    df[col_out] = (df[col_in]/100 - (df[col_in]/100).astype(int))*100.*0.0166666667 + (df[col_in]/100).astype(int)
    return df

def wgs84_to_web_mercator(df, lon, lat):
    """Converts decimal longitude/latitude to Web Mercator format"""
    k = 6378137
    df['wm%s'%lon] = df[lon] * (k * np.pi/180.0)
    df['wm%s'%lat] = np.log(np.tan((90 + df[lat]) * np.pi/360.0)) * k
    return df

def read_prepare_data(ship):
    """Uses all data tools above to deliver the final cleaned DataFrame"""
    ##FIXME! a whole bunch of hard-coded specifications here!
    if ship.lower() == 'fushimi':
        filename = '../nykfushimi@nyk.dualog.net_output_combined.csv'
        sr = 0
        long1, lat1 = '2008', '2000'
        long2, lat2 = '2012', '2004'
    elif ship.lower() == 'diamond':
        filename = '../acxdiamond@nyk.dualog.net_output_combined.csv'
        sr = 9
        long1, lat1 = '1034', '1026'
        long2, lat2 = '1038', '1030'
    df = pd.read_csv(filename, header=None, parse_dates=[0,1], skiprows=sr)
    df['timestamp2'] = pd.to_datetime(df[0])
    df['timestamp1'] = pd.to_datetime(df[1])
    df = clean(df, ship)
    df = convert_coordinate(df, lat1, 'lat1')
    df = convert_coordinate(df, long1, 'long1')
    df = convert_coordinate(df, lat2, 'lat2')
    df = convert_coordinate(df, long2, 'long2')
    df = scale_impute(df, 'mean')
    df = wgs84_to_web_mercator(df, 'long1', 'lat1')
    df = wgs84_to_web_mercator(df, 'long2', 'lat2')
    df['timestamp_date'] = df['timestamp1'].dt.strftime('%Y-%m-%d')
    return df

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

##### Organized #####
    

app = MyApp(graph_item_width=400, graph_item_height=200)
t1=timeseries(app, 'foo', (0,0))
