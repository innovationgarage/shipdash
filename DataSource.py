import pandas as pd

class DataSource(object):
    dsrc_types = {
        "csv": pd.read_csv,
        "json": pd.read_json
    }

    def __init__(self, app, dsrc_name):
        self.app = app
        self.dsrc_name = dsrc_name

    def update_data(self, attrname, old, new): ##Needs list of widgets and list of dsrc columns
        
##FIXME!
        # Get the current slider values
        from_ind = from_slider.value
        to_ind = to_slider.value
        feature_ts_select = feature_ts_selector.value
        feature_ts2_select = feature_ts2_selector.value
        x_select = x_selector.value
        y_select = y_selector.value
    
        # Generate the new curve
        long1 = df['long1'][from_ind:to_ind]
        lat1 = df['lat1'][from_ind:to_ind]
        wmlong1 = df['wmlong1'][from_ind:to_ind]
        wmlat1 = df['wmlat1'][from_ind:to_ind]
        timestamp1 = df['timestamp1'][from_ind:to_ind]
        timestamp_date = df['timestamp_date'][from_ind:to_ind]
        feature_ts = df[feature_ts_select][from_ind:to_ind]
        feature_ts2 = df[feature_ts2_select][from_ind:to_ind]
        x = df[x_select][from_ind:to_ind]
        y = df[y_select][from_ind:to_ind]
        
        source.data = dict(
            long1=long1, lat1=lat1,
            wmlong1=wmlong1, wmlat1=wmlat1,        
            timestamp1=timestamp1,
            feature_ts=feature_ts,
            feature_ts2=feature_ts2,
            x=x, y=y,
            timestamp_date=timestamp_date,
        )
        
