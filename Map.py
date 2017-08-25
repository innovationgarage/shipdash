import bokeh.plotting as bp
import bokeh.tile_providers
import GraphElement

class Map(GraphElement.GraphElement):

    def __init__(self, app, id, title, width=1, height=1):
        GraphElement.GraphElement.__init__(self, app, id, title)
        x_range = (13884029, 12553304)
        y_range = (-2698291, 6455972)
        url = 'http://c.tile.openstreetmap.org/{Z}/{X}/{Y}.png'
        attribution = ""
        self.width = width
        self.height = height
        self.graph = bp.figure(
            x_range = x_range,
            y_range = y_range,
            plot_width = int(self.app.graph_item_width * self.width),
            plot_height = int(self.app.graph_item_height * self.height),
        )
        self.tile = self.graph.add_tile(bokeh.tile_providers.WMTSTileSource(url=url, attribution=attribution))
        self.draw()

    def draw_dsrc(self, dsrc):
        self.draw_path(dsrc)

    def save(self):
        res = GraphElement.GraphElement.save(self)
        res['args']['width'] = self.width
        res['args']['height'] = self.height
        return res

GraphElement.GraphElement.types['Map'] = Map
