### TEVdata.py ###
# This file contains helpful classes and data used by the dashboard

# Imports
import pandas as pd

# TEVdata object
# Used to store data and return manipulated data
class TEVdata():
    def __init__(self, datasource, graphtype):
        self.ds = datasource
        self.graph_type = graphtype

        # Retrieve and clean data
        self.df = pd.read_csv(self.ds)
        self.df['iso3_code'] = self.df['iso3_code'].str.upper()

        self.countries = self.df['iso3_code'].unique()
        self.types = self.df['type'].unique()
        self.species = self.df['category'].unique()
        self.max_year = int(self.df['year'].max())
        self.min_year = int(self.df['year'].min())
    
    def filter_country(self, code, df):
        if code is None:
            return df
        return df[df['iso3_code']==code]
    
    def filter_type(self, type, df):
        if type is None:
            return df
        return df[df['type']==type]
    
    def filter_species(self, spec, df):
        if spec is None:
            return df
        return df[df['category']==spec]