import bokeh.plotting as bp
import bokeh.layouts as bl

class GraphElement(object):

    def __init__(self, app, id='', title=''):
        self.app = app
        self.id = id        
        self.title = title

    types = {}

    @classmethod
    def load(cls, app, config):
        return cls.types[config['type']](app=app, **config['args'])
        # try:
        #     return cls.types[config['type']](app=app, **config['args'])
        # except Exception, e:
        #     import pdb, sys
        #     sys.last_traceback = sys.exc_info()[2]
        #     pdb.pm()
    
    def draw(self):
        self.graphs = []
        for dsrc in self.app.get_dsrcs():
            self.graphs.append(
                self.draw_dsrc(dsrc)
            )

    def draw_dsrc(self, dsrc):
        import pdb
        pdb.set_trace()

    def draw_path(self, dsrc):
        return self.graph.line("%s:longitude" % self.id, "%s:latitude" % self.id, source=dsrc)

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

class Row(GraphElement):
    graph_type = bl.row
    def __init__(self, app, children, **arg):
        GraphElement.__init__(self, app, **arg)
        self.children = [GraphElement.load(app, child) for child in children]
        self.graph = bl.row([child.graph for child in self.children])

    def draw(self):
        for child in self.children:
            child.draw()

GraphElement.types['Row'] = Row    

class Column(GraphElement):
    graph_type = bl.column
    def __init__(self, app, children, **arg):
        GraphElement.__init__(self, app, **arg)
        self.children = [GraphElement.load(app, child) for child in children]
        self.graph = bl.column([child.graph for child in self.children])

    def draw(self):
        for child in self.children:
            child.draw()

GraphElement.types['Column'] = Column    
