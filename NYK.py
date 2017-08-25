import json
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None
from sklearn.preprocessing import Imputer, StandardScaler
import DataSource
import os.path

class NYK(DataSource.DataSource):

    def __init__(self, app, dsrc_name='', dsrc_type='csv', dsrc_path='data/', file_name='', header_rows=None, date_cols=None, skip_rows=None, lat1=None, long1=None, lat2=None, long2=None):
        DataSource.DataSource.__init__(self, app, dsrc_name)
        self.dsrc_type = dsrc_type
        self.dsrc_path = dsrc_path
        self.file_name = file_name
        self.header_rows = header_rows
        self.date_cols = date_cols
        self.skip_rows = skip_rows
        self.lat1 = lat1
        self.long1 = long1
        self.lat2 = lat2
        self.long2 = long2
        self.read_prepare_data()
        self.init_dsrc()

    """These methods are fine-tuned for the current data sets. I need to
    generalize them once I know more about different types of data coming
    in"""

    @classmethod
    def clean(cls, df, name):
        """Find all empty space or all NaN columns and drops them from the DataFrame"""
        df.replace(r'\s+', np.nan, regex=True, inplace=True)
        df.replace(r'-', np.nan, regex=True, inplace=True)
        df.dropna(axis=1, how='all', inplace=True)
        df.columns = [str(x) for x in df.columns]
        df.reset_index(level=[0], inplace=True)
        df.rename(columns={'index': 'ind'}, inplace=True)
        """This is to find coordinate columns etc. manually, because we don't
        know anything about the structure of our data!"""
#         df.to_csv('data/'+name+'_clean.csv')
        return df
    
    @classmethod
    def scale_impute(cls, df, method):
        """Find float columns, impute their NaN values with 'method', and then min-max scale the column/feature"""
        fill_NaN = Imputer(missing_values=np.nan, strategy=method, axis=1)
        df[df.loc[:, df.dtypes == 'float64'].columns.difference(['lat1', 'long1', 'lat2', 'long2'])] = fill_NaN.fit_transform(
            df[df.loc[:, df.dtypes == 'float64'].columns.difference(['lat1', 'long1', 'lat2', 'long2'])]
        )    
        scaler = StandardScaler()
        df[df.loc[:, df.dtypes == 'float64'].columns.difference(['lat1', 'long1', 'lat2', 'long2'])] = scaler.fit_transform(
            df[df.loc[:, df.dtypes == 'float64'].columns.difference(['lat1', 'long1', 'lat2', 'long2'])]
        )
        return df

    @classmethod    
    def convert_coordinate(cls, df, col_in, col_out):
        """Convert coordinates of the format [d]ddmm.mmm to [dd]d.ddd"""
        ##FIXME! This is assuming all coordinates are E and N 
        df[col_out] = (df[col_in]/100 - (df[col_in]/100).astype(int))*100.*0.0166666667 + (df[col_in]/100).astype(int)
        return df

    @classmethod    
    def wgs84_to_web_mercator(cls, df, lon, lat):
        """Convert decimal longitude/latitude to Web Mercator format"""
        k = 6378137
        df['wm%s'%lon] = df[lon] * (k * np.pi/180.0)
        df['wm%s'%lat] = np.log(np.tan((90 + df[lat]) * np.pi/360.0)) * k
        return df
        
    def read_prepare_data(self):
        """Use all data tools above to deliver the final cleaned DataFrame"""
        self.data = self.dsrc_types[self.dsrc_type](
            os.path.join(self.dsrc_path, self.file_name),
            header = self.header_rows,
            parse_dates = self.date_cols,
            skiprows = self.skip_rows,
            error_bad_lines = False,
            low_memory = False
        )

        self.data['timestamp2'] = pd.to_datetime(self.data[0])
        self.data['timestamp1'] = pd.to_datetime(self.data[1])
        self.clean(self.data, self.dsrc_name)
        self.convert_coordinate(self.data, str(self.lat1), 'lat1')
        self.convert_coordinate(self.data, str(self.long1), 'long1')
        self.convert_coordinate(self.data, str(self.lat2), 'lat2')
        self.convert_coordinate(self.data, str(self.long2), 'long2')
        self.scale_impute(self.data, 'mean')
        self.wgs84_to_web_mercator(self.data, 'long1', 'lat1')
        self.wgs84_to_web_mercator(self.data, 'long2', 'lat2')
        self.data['timestamp_date'] = self.data['timestamp1'].dt.strftime('%Y-%m-%d')

DataSource.DataSource.types['NYK'] = NYK
