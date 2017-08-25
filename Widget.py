import bokeh.models.widgets
import GraphElement

class Widget(GraphElement.GraphElement):
    def __init__(self, app, id, title, width=1, height=0.1, **widget_config):
        GraphElement.GraphElement.__init__(self, app, id, title)
        self.width = width
        self.height = height
        self.width = width
        self.height = height
        self.config = widget_config
        self.graph = self.graph_type(
            title=self.title,
            width=int(self.app.graph_item_width * self.width),
            height=int(self.app.graph_item_height * self.height),
            **widget_config)
        self.graph.on_change('value', self.update)

    def draw(self):
        pass
    
class Select(Widget):
    graph_type = bokeh.models.widgets.Select
    def __init__(self, app, id, title, width=1, height=0.1, mapping="", **widget_config):
        self.mapping = mapping
        relevant_data = app.data_sources['Fushimi'].dsrc.data
        Widget.__init__(self, app, id, title, width, height,
                        options = ['12', 'lat1', 'lat2', 'long1', 'long2'], ##FIXME!! Hard-coded crap!
                        **widget_config)
    
    def update(self, attrname, old, new):
        self.app.mapping[self.mapping] = new
        self.app.update_dsrcs()

GraphElement.GraphElement.types['Select'] = Select


class Slider_from(Widget):
    graph_type = bokeh.models.widgets.Slider
    def __init__(self, app, id, title, width=1, height=0.1, mapping="", **widget_config):
        self.mapping = mapping
        Widget.__init__(self, app, id, title, width, height,
                        start = app.range['from'],
                        end = app.range['to'],
                        value = 1, ##FIXME!! Hard-coded crap!
                        step = 1, ##FIXME!! Hard-coded crap!
                        **widget_config)

    def update(self, attrname, old, new):
        self.app.range['from'] = new
        self.app.update_dsrcs()

GraphElement.GraphElement.types['Slider_from'] = Slider_from


class Slider_to(Widget):
    graph_type = bokeh.models.widgets.Slider
    def __init__(self, app, id, title, width=1, height=0.1, mapping="", **widget_config):
        self.mapping = mapping
        Widget.__init__(self, app, id, title, width, height,
                        start = app.range['from'],
                        end = app.range['to'],
                        value = 1,
                        step = 1,
                        **widget_config)

    def update(self, attrname, old, new):
        self.app.range['to'] = new
        self.app.update_dsrcs()

GraphElement.GraphElement.types['Slider_to'] = Slider_to
