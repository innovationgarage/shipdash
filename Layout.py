from bokeh.layouts import column, row

class Layout(object):
    layout_types = {
        "row": row,
        "column": column
    }
    
    def __init__(self, app, children, layout_type):
        self.children = children
        self.layout_type = layout_type
        self.layout = self.layout_types[self.layout_type](self.children)
    
        
