import bokeh.plotting as bp
from bokeh.tile_providers import WMTSTileSource
import GraphElement

class Map(GraphElement.GraphElement):

    def __init__(self, app, graph_id, graph_title, width=1, height=1):
        GraphElement.GraphElement.__init__(self, app, graph_id, graph_title)
        self.x_range = (13884029, 12553304)
        self.y_range = (-2698291, 6455972)
        self.url = 'http://c.tile.openstreetmap.org/{Z}/{X}/{Y}.png'
        self.attribution = ""
        self.width = width
        self.height = height
        self.graph = bp.figure(
            x_range = self.x_range,
            y_range = self.y_range,
            plot_width = int(self.app.graph_item_width * self.width),
            plot_height = int(self.app.graph_item_height * self.height),
        )
        self.graph.add_tile(WMTSTileSource(url=self.url, attribution=self.attribution))
        
    def draw_path(self, lon, lat, dsrc, **kwargs):
        self.lon = lon
        self.lat = lat
        self.dsrc = dsrc
        self.style = "path"
        return self.graph.line(self.lon, self.lat, source=self.dsrc)

    def save(self):
        res = GraphElement.GraphElement.save(self)
        res['type'] = 'Map'
        res['args']['width'] = self.width
        res['args']['height'] = self.height
        return res