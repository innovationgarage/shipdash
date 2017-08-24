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

test = False

shipapp = App.App()
data_source = NYK.NYK(shipapp, "Fushimi", "csv", "data/")
df = data_source.data

shipmap = Map.Map(shipapp, 'shipmap', 'shipmap')
shipmap.draw_path('wmlong1', 'wmlat1', df)
#shipmap.show()

shipts = Timeseries.Timeseries(shipapp, 'shipts', 'shipts')
shipts.draw_line('timestamp1', 'lat1', df)
#shipts.show()

shipscatter = Scatter.Scatter(shipapp, 'shipscatter', 'shipscatter')
shipscatter.draw_scatter('wmlong2', 'wmlat2', df)
#shipscatter.show()

slider_from = Widget.Widget(shipapp, 'sliderf', 'sliderf', 'Slider_from', value=0, start=0, end=len(df), step=1)
slider_to = Widget.Widget(shipapp, 'slidert', 'slidert', 'Slider_to', value=0, start=0, end=len(df), step=1)
select = Widget.Widget(shipapp, 'select', 'select', 'Select', options=list(df.loc[:,df.dtypes == 'float64'].columns))

bp.output_file('GraphElements.html')
bp.show(
    row(
        column(slider_from.graph,
               slider_to.graph,
               select.graph,
        ),
        column(
            row(shipmap.graph,
                shipscatter.graph
            ),
            shipts.graph
        )
    )
)


if test:
    import bokeh.plotting as bp
    from bokeh.tile_providers import WMTSTileSource
    bp.output_file('tst.html')
    f1 = bp.figure()
    f1.circle('wmlong2', 'wmlat2', source=df)
    f2 = bp.figure()
    url = 'http://c.tile.openstreetmap.org/{Z}/{X}/{Y}.png'
    attribution = ""#Map tiles by Carto, under CC BY 3.0. Data by OpenStreetMap, under ODbL"
    f2.add_tile(WMTSTileSource(url=url, attribution=attribution))
    f2.line('wmlong1', 'wmlat1', source=df)
    f3 = bp.figure()
    f3.line('timestamp1', 'lat1', source=df)
    bp.show(row(f1,f2,f3))
