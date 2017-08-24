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

with open(sys.argv[1]) as f:
    config = json.load(f)

App.App(**config)
