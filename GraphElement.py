import bokeh.plotting as bp
from bokeh.tile_providers import WMTSTileSource

class GraphElement(object):

    def __init__(self, app, graph_id, graph_title):
        self.app = app
        self.graph_title = graph_id        
        self.graph_title = graph_title
    
    def draw_line(self, t, x, dsrc, **kwargs):
        self.t = t
        self.x = x
        self.dsrc = dsrc
        self.graph.line(self.t, self.x, source=self.dsrc, **kwargs)
        self.style = "line"

    def draw_scatter(self, x, y, dsrc):
        self.x = x
        self.y = y
        self.dsrc = dsrc
        self.graph.circle(self.x, self.y, source=self.dsrc)
        self.style = "circle"

    def save(self):
        return {
            "args": {
                "id": self.graph_id,
                "title": self.graph_title,
            },
            "details": []
        }

    def rm(self):
        pass

    def update(self):
        pass
        
    def show(self):
        self.output_file = 'graph_element.html'
        bp.output_file(self.output_file)
        bp.show(self.graph)

    def flatten_graph_elements():
        return [self]
    
