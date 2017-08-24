import bokeh.plotting as bp
from bokeh.tile_providers import WMTSTileSource

class GraphElement(object):

    def __init__(self, app, graph_id, graph_title):
        self.app = app
        self.graph_title = graph_id        
        self.graph_title = graph_title
        self.draw()

    types = {}

    @classmethod
    def load(cls, config):
        return cls.types[config['type']](**config['args'])
    
    def draw(self):
        self.graphs = []
        for dsrc in self.app.get_dsrcs():
            self.graphs.append(
                self.draw_dsrc(dsrc)
            )

    def draw_dsrc(self, dsrc):
        raise NotImplemented

    def draw_line(self, dsrc):
        return self.graph.line("%s:x" % self.id, "%s:y" % self.id, source=dsrc)

    def draw_scatter(self, dsrc):
        return self.graph.circle("%s:x" % self.id, "%s:y" % self.id, source=dsrc)

    def save(self):
        return {
            "type": type(self).__name__,
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
    
