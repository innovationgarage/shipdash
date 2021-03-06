import bokeh.plotting as bp
import data_tools as dtools
import GraphElement
import DataSource
import Map
import Scatter
import Timeseries

class App(object):
    graph_types = {
        "Map": Map,
        "Timeseries": Timeseries,
        "Scatter": Scatter
    }

    def __init__(self, data, active_data, mapping, range, layout, graph_item_width=400, graph_item_height=400):
        self.graph_item_width = graph_item_width
        self.graph_item_height = graph_item_height

        self.mapping = mapping
        self.range = range
        self.data_sources = {name: DataSource.DataSource.load(self, cfg) for name, cfg in data.iteritems()}
        self.active_data = active_data
        self.layout = GraphElement.GraphElement.load(self, layout)
        self.layout.draw()
        bp.curdoc().add_root(self.layout.graph)
        
    def get_dsrcs(self):
        for active_data in self.active_data:
            yield self.data_sources[active_data].dsrc

    def update_dsrcs(self):
        for data_source in self.data_sources.values():
            data_source.update_dsrc()

    def init_graph_element(config):
        return graph_types[config['type']](**config['args'])

    def init_layout(self, config):
        self.layout = make_graph_element(config)
        self.graph_elements = self.layout.flatten_graph_elements()
            
    def draw_in_graph(self, graph_id, graph_style, **graph_params):
        self.graph_elements[graph_id].graph_styles[graph_style](**graph_params)

    def init_widgets(self):
        pass

    def update_data(self):
        pass

    def setup_layout(self):
        pass

    def save(self):
        return {
            "type": "App",
            "args": {
                "graph_item_width": self.graph_item_width,
                "graph_item_height": self.graph_item_height
            }
        }
    
