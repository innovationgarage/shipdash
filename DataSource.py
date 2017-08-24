import pandas as pd

class DataSource(object):
    dsrc_types = {
        "csv": pd.read_csv,
        "json": pd.read_json
    }

    def __init__(self, app, dsrc_name):
        self.app = app
        app.data = self
        self.dsrc_name = dsrc_name

    types = {}

    @classmethod
    def load(cls, config):
        return cls.types[config['type']](**config['args'])

    def init_dsrc(self):
        self.dsrc = ColumnsDataSource(data={})
        for col in self.app.mapping.keys():
            self.dsrc.add([], col)

    def update_dsrc(self):
        for key, value in self.app.mapping.iteritems():
            if value in self.data.columns:
                self.dsrc.data[key] = self.data[value][self.app.range['from']:self.app.range['to']]
            else:
                self.dsrc.data[key] = [] # FIXME: make a real empty pandas dataframe column to stick here...
