### TEVdata.py ###
# This file contains helpful classes and data used by the dashboard

# Imports
import numpy
import pandas as pd

# TEVdata object
# Used to store data and return manipulated data
class TEVdata():
    def __init__(self, datasource):
        self.ds = datasource

        # Retrieve and clean data
        self.df = pd.read_csv(self.ds)
        self.df['iso3_code'] = self.df['iso3_code'].str.upper()

        self.df.rename(columns={
            'year':'Year', 
            'iso3_code':'Country',
            'category':'Species',
            'value':'Value', 
            'type':'Type', 
            'unit':'Currency',
        }, inplace=True)

        self.countries = sorted(self.df['Country'].unique())
        self.types = self.df['Type'].unique()
        self.types = numpy.delete(self.types, numpy.where(self.types == 'Crops'))
        self.species = self.df['Species'].unique()
        self.max_year = int(self.df['Year'].max())
        self.min_year = int(self.df['Year'].min())
    
    def filter_country(self, code, df):
        if code is None or len(code) == 0:
            return df
        if isinstance(code,list):
            return df[df['Country'].isin(code)]
        return df[df['Country']==code]
    
    def filter_type(self, type, df):
        if type is None:
            return df
        return df[df['Type']==type]
    
    def filter_species(self, spec, df):
        if spec is None:
            return df
        return df[df['Species']==spec]
    
    def filter_year(self, year, df):
        if year is None:
            return df
        year = int(year)
        return df[df['Year']==year]

    def convert_country_codes(self, code_file):
        codes = pd.read_csv(code_file)

        # line inspired by answer on SO https://stackoverflow.com/a/53118885
        self.df['Country'] = self.df['Country'].replace(dict(zip(codes['ISO3'], codes['Menu Name'])))
        self.countries = sorted(self.df['Country'].unique())
        
        return