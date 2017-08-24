
def interpret_config(config_file):
    import json
    with open(config_file) as f:
        conf = json.load(f)
    
#################
graph_types = {
    "Map": Map,
    "Timeseries": Timeseries,
    "Scatter": Scatter
}

def make_graph_element(config):
    return graph_type[config['type']](**config['args'])

x = Scatter(..)
with open("foo.json", "w") as f:
    json.dump(x.save(), f)

with open("foo.json") as f:
    y = make_graph(json.load(f))

