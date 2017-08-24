from bokeh.models.sources import ColumnDataSource
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
    graph_styles = {
        "line": GraphElement.GraphElement.draw_line,
        "scatter": GraphElement.GraphElement.draw_scatter,
        "path": Map.Map.draw_path
    }

    def __init__(self, graph_item_width=400, graph_item_height=400):
        self.graph_item_width = graph_item_width
        self.graph_item_height = graph_item_height

    def init_dsrc(self, *columns):
        """All plots start by having no data plotted in them. However,
        we need a dsrc to later use to populate the plots with. These
        column names should come from the config file"""
        self.dsrc = ColumnsDataSource(data={})
        for col in columns:
            self.dsrc.add([], col)

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

# x = Scatter(..)
# with open("foo.json", "w") as f:
#     json.dump(x.save(), f)

# with open("foo.json") as f:
#     y = make_graph(json.load(f))
    
