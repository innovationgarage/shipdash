from bokeh.models.widgets import Slider, Select
import GraphElement

class Widget(GraphElement.GraphElement):
    widget_types = {
#        "RangeSlider": #FIXME!
        "Slider_from": Slider,
        "Slider_to": Slider,        
        "Select": Select,
    }
    
    def __init__(self, app, graph_id, graph_title, graph_type, width=1, height=0.1, **widget_config):
        GraphElement.GraphElement.__init__(self, app, graph_id, graph_title)
        self.width = width
        self.height = height
        self.graph_type = graph_type
        self.width = width
        self.height = height
        self.config = widget_config
        self.graph = self.widget_types[self.graph_type](
            title=self.graph_title,
            width=int(self.app.graph_item_width * self.width),
            height=int(self.app.graph_item_height * self.height),
            **widget_config)

