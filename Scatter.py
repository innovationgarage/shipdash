import bokeh.plotting as bp
import GraphElement

class Scatter(GraphElement.GraphElement):

    def __init__(self, app, id, title, width=1, height=1):
        GraphElement.GraphElement.__init__(self, app, id, title)
        self.width = width
        self.height = height
        self.graph = bp.figure(
            plot_width = int(self.app.graph_item_width * self.width),
            plot_height = int(self.app.graph_item_height * self.height),
        )
        
    def draw_dsrc(self, dsrc):
        self.draw_scatter(dsrc)

    def save(self):
        res = GraphElement.GraphElement.save(self)
        res['args']['width'] = self.width
        res['args']['height'] = self.height
        return res

GraphElement.GraphElement.types['Scatter'] = Scatter
