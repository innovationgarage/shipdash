from bokeh.models import widgets
import bokeh.plotting as bp
from bokeh.layouts import column, row, gridplot, widgetbox, layout
import pandas as pd
import data_tools as dtools
import App
import Map
import Timeseries
import Scatter
import Widget
import DataSource
import NYK
import sys
import json

with open('dash_config.json') as f:
    config = json.load(f)

shipapp = App.App(**config)
