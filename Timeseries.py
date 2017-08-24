import bokeh.plotting as bp
import GraphElement

class Timeseries(GraphElement.GraphElement):

    def __init__(self, app, graph_id, graph_title, width=2, height=0.5):
        GraphElement.GraphElement.__init__(self, app, graph_id, graph_title)
        self.width = width
        self.height = height
        self.graph = bp.figure(
            x_axis_type = "datetime",
            plot_width = int(self.app.graph_item_width * self.width),
            plot_height = int(self.app.graph_item_height * self.height),
        )

    def draw_dsrc(self, dsrc):
        self.draw_line(dsrc)

    def save(self):
        res = GraphElement.GraphElement.save(self)
        res['args']['width'] = self.width
        res['args']['height'] = self.height
        return res

GraphElement.GraphElement.types['Timeseries'] = Timeseries
