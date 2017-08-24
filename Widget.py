import bokeh.models.widgets # import Slider, Select
import GraphElement

class Widget(GraphElement.GraphElement):
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
        self.graph.on_change('value', self.update)

    def update(self, attrname, old, new):

class Select(Widget):
    graph_type = bokeh.models.widgets.Select
    def __init__(self, app, graph_id, graph_title, graph_type, width=1, height=0.1, mapping="", **widget_config):
        self.mapping = mapping
        Widget.__init__(self, app, graph_id, graph_title, graph_type, width, height, widget_config)
    
    def update(self, attrname, old, new):
        self.app.mapping[self.mapping] = new
        self.app.update_dsrcs()

GraphElement.GraphElement.types['Select'] = Select


class Slider_from(Widget):
    graph_type = bokeh.models.widgets.Slider

    def update(self, attrname, old, new):
        self.app.rage['from'] = new
        self.app.update_dsrcs()

GraphElement.GraphElement.types['Slider_from'] = Slider_from


class Slider_to(Widget):
    graph_type = bokeh.models.widgets.Slider

    def update(self, attrname, old, new):
        self.app.rage['to'] = new
        self.app.update_dsrcs()

GraphElement.GraphElement.types['Slider_to'] = Slider_to
