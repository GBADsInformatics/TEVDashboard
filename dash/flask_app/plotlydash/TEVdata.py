### TEVdata.py ###
# This file contains helpful classes and data used by the dashboard

# Imports
import math
import numpy
import pandas as pd

# Metadata constants
METASET = 'datasets/metadata/'
AWS_BUCKET = 'https://gbads-metadata.s3.ca-central-1.amazonaws.com/'

METADATA_SOURCES = {
    'FAOSTAT QCL':{
        'METADATA': METASET+'FAOSTAT_QCL.csv',
        'DOWNLOAD': AWS_BUCKET+'20220613_FAOSTAT_QCL.json',
        'PROVENANCE': METASET+'FAOSTAT_QCL_PROVENANCE.txt',
    },
    'FAO FISHSTAT J':{
        'METADATA': METASET+'20220719_FAO_FISHSTATJ.csv',
        'DOWNLOAD': AWS_BUCKET+'20220613_FAOSTAT_QCL.json',
        # 'DOWNLOAD': AWS_BUCKET+'20220719_FAO_FISHSTATJ.json',
        'PROVENANCE': METASET+'FAO_FISHSTATJ_PROVENANCE.txt',
    },
}
METADATA_OTHER = {
    'GLOSSARY':{
        'CSV': METASET+'MetadataGlossary.csv',
    },
}

# Code from SA: https://stackoverflow.com/q/3154460
NumberWords = ['',' Thousand',' Million',' Billion',' Trillion']
def humanize(n):
    n = float(n)
    magnitude = max(0,min(len(NumberWords)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))
    return '{:.2f}{}'.format(n / 10**(3 * magnitude), NumberWords[magnitude])

# TEVdata object
# Used to store data and return manipulated data
class TEVdata():
    def __init__(self, datasource,iso3codes):
        self.ds = datasource
        codes = pd.read_csv(iso3codes)

        # Retrieve and clean data
        self.df = pd.read_csv(self.ds)
        self.df['iso3_code'] = self.df['iso3_code'].str.upper()
        
        # Adding ISO3 column, and converting iso3_code to 'country menu names'
        self.df['ISO3'] = self.df['iso3_code']
        self.df['iso3_code'] = self.df['ISO3'].replace(dict(zip(codes['ISO3'], codes['Menu Name'])))

        self.df.rename(columns={
            'year':'Year',
            'iso3_code':'Country',
            'category':'Species',
            'value':'Value', 
            'type':'Type', 
            'unit':'Currency',
        }, inplace=True)


        # Replacing asset value with live animals
        self.df.loc[(self.df['Type'] == 'Asset'),'Type']='Live Animals'

        # Adding total value
        testdf = self.df.groupby(['Year','Country','Species','Currency','ISO3'],as_index=False)['Value'].sum()
        # Adding type column back
        testdf['Type'] = 'Total'
        # Deleting aquaculture rows (these rows only have Output types, so Total and Output types would be the same)
        testdf = testdf.drop(testdf[testdf['Species'] == 'Aquaculture'].index)
        # Adding total to original df
        self.df = pd.concat([self.df,testdf],ignore_index=True)

        # Adding formatted code
        self.df['Human'] = self.df['Value'].apply(lambda x : humanize(x))

        self.countries = sorted(self.df['Country'].unique())
        self.types = self.df['Type'].unique()
        self.types = numpy.delete(self.types, numpy.where(self.types == 'Crops'))
        self.species = self.df['Species'].unique()
        self.max_year = int(self.df['Year'].max())
        self.min_year = int(self.df['Year'].min())
    
    def filter_country(self, code, df, default):
        if code is None or len(code) == 0:
            code = [default]
        if code is None or len(code) == 0:
            return df[df['Type']=='ThisReturnsEmptyDF']
        code = list(code)
        if 'All' in code:
            return df
        return df[df['Country'].isin(code)]
        
    def filter_type(self, type, df, default):
        if type is None:
            type = default
        if type is None:
            return df[df['Type']=='ThisReturnsEmptyDF']
        if type == 'All':
            return df
        return df[df['Type']==type]
    
    def filter_species(self, spec, df, default):
        if spec is None:
            spec = default
        if spec is None:
            return df[df['Type']=='ThisReturnsEmptyDF']
        if spec == 'All':
            return df
        return df[df['Species']==spec]
    
    def filter_year(self, year, df):
        if year is None:
            return df
        year = int(year)
        return df[df['Year']==year]
