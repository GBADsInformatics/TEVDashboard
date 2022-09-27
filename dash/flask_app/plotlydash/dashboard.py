import json
from logging import disable
from os.path import exists
import requests
import numpy as np
import pandas as pd
import math
import urllib.parse
import dash
from dash import dcc,html,dash_table,callback_context
import dash_bootstrap_components as dbc
import plotly.express as px
from datetime import date, datetime
from functools import wraps
from flask import session, redirect
import plotly.graph_objects as go
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from dash.exceptions import PreventUpdate
from layouts import *
from dash.dependencies import Input, Output, State
# from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform
import json
from textwrap import dedent
from .TEVdata import *

# Chloropleth map country data
from urllib.request import urlopen
plotly_countries = {}
with open("datasets/world_map_110m.geojson") as file:
    plotly_countries = json.load(file)

# Where to get the table dataset from
import urllib.request
try:
    urllib.request.urlretrieve("http://gbadskedoc.org/api/tevHook", "datasets/tev_data.csv")
except:
    print('ERROR: http://gbadskedoc.org/api/tevHook threw an exception.')

# Creating Dataset
tevdata = TEVdata('datasets/tev_data.csv' if exists("datasets/tev_data.csv") else 'datasets/tev_data_backup.csv','datasets/adminunits.csv')

stylesheet = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css'
]

PROFILE_KEY = 'profile'
JWT_PAYLOAD = 'jwt_payload'

def init_dashboard(server):
            
    dash_app = dash.Dash(__name__,
        server=server,
        title='TEV Dashboard',
        routes_pathname_prefix="/dash/",
        external_stylesheets=[
            # 'https://codepen.io/chriddyp/pen/bWLwgP.css',
            dbc.themes.BOOTSTRAP,
            dbc.icons.BOOTSTRAP
        ],
    )
    # Setting active page
    dash_app.layout = html.Div([
        dcc.Location(id='url', refresh=False)
    ],id='page-content')
    init_callbacks(dash_app)
    return dash_app.server

isLoggedIn = False
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        global isLoggedIn
        if PROFILE_KEY not in session:
            isLoggedIn = False
            return redirect('/login')
        isLoggedIn = True
        return f(*args, **kwargs)
    return decorated

def checkRole():
    isRole = False
    y = json.dumps(session[JWT_PAYLOAD])
    person_dict = json.loads(y)
    p = (person_dict["http://gbad.org/roles"]) # This link sends you to the Ground Based Air Defense website lmao
    stringver = json.dumps(p)
    print(stringver)
    if 'Verified User' in stringver:
        isRole = True
    else:
        isRole = False
    return isRole

def getJWT(personDict,userCat):
    p = (personDict[userCat])
    stringVer = json.dumps(p)
    s1 = stringVer.replace("[]","")
    strippedString = s1.strip('"')
    return strippedString

@requires_auth
def getUserContent():
    y = json.dumps(session[JWT_PAYLOAD])
    personDict = json.loads(y)
    userEmail = getJWT(personDict,"email")
    print(userEmail)
    return userEmail

##CALLBACKS -------------------------------------------------------------------------------------------------------------------------------------------------------------
def init_callbacks(dash_app):
    
    # Callbacks to handle login components
    @dash_app.callback(
        Output(component_id='login-button', component_property='style'),
        Input('url', 'pathname')
    )
    @requires_auth
    def login_button(pathname):
        checkRole()
        return {'margin-left': '5px', 'display': 'none'}
    
    @dash_app.callback(
        Output(component_id='logout-button', component_property='style'),
        Input('url', 'pathname')
    )
    @requires_auth
    def logout_button(pathname):
        return {'margin-top': '10px', 'margin-right':'10px', 'float': 'right'}

    # Callback to handle feedback.
    @dash_app.callback(
        Output('feedback-text', 'value'),
        Output('feedback-button', 'disabled'),
        Output('feedback-text', 'disabled'),
        Input("feedback-button", "n_clicks"),
        State('feedback-text', 'value')
    )
    def feedback_box(n, text):
        if (n > 0 and text != None and text != ""):
            outF = open("feedback.txt", "a")
            outF.writelines('["'+text+'"]\n')
            outF.close()
            return\
                "Thank you for your feedback",\
                True,\
                True
        else:
            print("no")
    
    # Callback to handle changing the page based on the pathname provided.
    @dash_app.callback(
        Output('page-content', 'children'),
        Input('url', 'pathname')
    )
    def display_page(pathname):
        if pathname == '/dash/':
            layout = page_1
        else:
            layout = "404"
        return layout

    ### Updating Dropdowns ###
    @dash_app.callback(
        Output('first-dropdown-title','children'),
        Output('country-dropdown','options'),
        Output('country-dropdown','style'),
        Output('year-input','style'),
        Output('year-input','min'),
        Output('year-input','max'),
        Output('livestock-or-asset-dropdown','options'),
        Output('livestock-or-asset-dropdown','clearable'),
        Output('species-dropdown','options'),
        Output('species-dropdown','clearable'),
        # Output('colour-dropdown','style'),
        # Output('colour-by-title','style'),
        Output('graph-type','data'),
        Input('area-graph','n_clicks'),
        Input('world-map','n_clicks'),
        State('species-dropdown','value'),
    )
    def update_dropdowns(_a,_b,species_value):
        # Getting Graph Type
        ctx = dash.callback_context
        if not ctx.triggered:
            button_id = 'No clicks'
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        # Setting variables based on graph type
        YearOrGeo,geoStyle,yearStyle,typeClearable,speciesClearable,graphType = None,None,None,None,None,None
        # YearOrGeo,geoStyle,yearStyle,typeClearable,speciesClearable,colourTitleStyle,colourStyle,graphType = None,None,None,None,None,None,None,None
        if button_id=="area-graph" or button_id=='No clicks':
            YearOrGeo = 'Geography'
            geoStyle = None
            yearStyle = {'display':'none'}
            typeClearable = True
            speciesClearable = True
            # colourStyle = None
            # colourTitleStyle = {"margin":"0.4rem 0 0.2rem 0"}
            graphType = 'line'
            countries = ['All'] + tevdata.countries
            categories = ['All'] + list(tevdata.types)
            species = ['All'] + list(tevdata.species)
        else:
            YearOrGeo = 'Year'
            geoStyle = {'display':'none'}
            yearStyle = None
            typeClearable = False
            speciesClearable = False
            # colourStyle = {'display':'none'}
            # colourTitleStyle = {'display':'none'}
            graphType = 'world'
            countries = tevdata.countries
            categories = list(tevdata.types)
            species = list(tevdata.species)

        # print(type(tevdata.countries))
        # print(type(tevdata.types))
        # print(type(tevdata.species))

        minyear = tevdata.min_year
        maxyear = tevdata.max_year

        return YearOrGeo,countries,geoStyle,yearStyle,minyear,maxyear,categories,typeClearable,species,speciesClearable,graphType
        # return YearOrGeo,countries,geoStyle,yearStyle,minyear,maxyear,categories,typeClearable,species,speciesClearable,colourStyle,colourTitleStyle,graphType


    ### Updating Figure ###
    @dash_app.callback(
        Output('main-graph-parent','children'),
        Output('livestock-or-asset-dropdown','disabled'),
        # Input('area-graph','n_clicks'),
        # Input('world-map','n_clicks'),
        Input('country-dropdown','value'),
        Input('year-input','value'),
        Input('livestock-or-asset-dropdown','value'),
        Input('species-dropdown','value'),
        # Input('colour-dropdown','value'),
        Input('graph-type','data'),
    )
    def render_figure(country,year,asset_type_value,species_value,graph_type):
        # Overriding asset type if crops
        asset_type = 'Crops' if species_value == 'Crops' else asset_type_value
        asset_type = 'Output' if species_value == 'Aquaculture' else asset_type

        # Filtering data with the menu values
        new_df = tevdata.df
        new_df = tevdata.filter_type(asset_type, new_df,None if graph_type == 'world' else 'All')
        new_df = tevdata.filter_species(species_value, new_df,None if graph_type == 'world' else 'All')
        if(graph_type=='world'):
            new_df = tevdata.filter_year(year, new_df)
        else:
            new_df = tevdata.filter_country(country, new_df,'All')

        # Deciding on how to colour the graph, this should be added as a dropdown later
        # with options like [auto, country, type, species_value]
        color_by = 'Species'
        if asset_type is None or asset_type == 'All': color_by = 'Type'
        if country is None or len(country) == 0 or len(country) > 1 or "All" in country : color_by = 'Country'

            
        # Building the world plot
        figure = None
        if(graph_type=='world'):
            max_value = 0
            min_value = 0 # int(new_df['value'].min())
            if new_df.shape[0] != 0:
                max_value = int(new_df['Value'].max())
            else:
                if species_value is None: species_value = 'None'
                if asset_type is None: asset_type = 'None'
            
            fig = px.choropleth_mapbox(
                new_df, 
                geojson=plotly_countries, 
                locations='ISO3',
                color='Value',
                range_color=(min_value,max_value),
                # hover_data=['Country', 'Value'],
                hover_data={'Country':True,'Human':True, 'Value':False},
                featureidkey='properties.ISO_A3_EH',
                color_continuous_scale='magma_r',
                center={'lat':19, 'lon':11},
                mapbox_style='carto-positron',
                opacity=0.5,
                zoom=1,
                title='World Map of '+species_value+' '+(asset_type+' ' if asset_type != 'Crops' else '')+'Value in '+str(year)+' (2014-2016 Constant USD $)',
            )
            fig.update_layout(
                margin={"r":5,"t":45,"l":5,"b":5},
                font=dict(
                    size=16,
                ),
                template='plotly_white'
            )
            fig.update_traces(hovertemplate=fig.data[0].hovertemplate.replace('Human','Value'))
            fig.layout.autosize = True
            figure = dcc.Graph(className='main-graph-size', id="main-graph", figure=fig)

        # Building the line graph
        else:
            # Creating graph title
            fig_title = \
                f'Economic Value of '+\
                f'{species_value if species_value != None else "Animal"} '+\
                f'{"" if asset_type == None or asset_type == "Crops" else asset_type + " "}'+\
                f'{"in All Countries" if country is None or len(country) == 0 or "All" in country else "in " + ",".join(new_df["Country"].unique())}'+\
                ' (2014-2016 Constant USD $)'

            fig = px.line(
                new_df, 
                x='Year',
                y='Value',
                color=color_by,
                title=fig_title,
                markers=True,
                hover_data={'Human':True, 'Value':False},
            )
            fig.update_layout(
                margin={"r":10,"t":45,"l":10,"b":10},
                font=dict(
                    size=16,
                ),
                template='plotly_white',
            )
            fig.update_traces(hovertemplate=fig.data[0].hovertemplate.replace('Human','Value'))
            fig.layout.autosize = True
            figure = dcc.Graph(className='main-graph-size', id="main-graph", figure=fig)

        # Returning graph
        typeDisabled = True if species_value == 'Crops' or species_value == 'Aquaculture' else False
        return figure,typeDisabled

    ### Updating Datatable and Alert###
    @dash_app.callback(
        Output('data-table-parent','children'),
        Output('alert-container','children'),
        Input('country-dropdown','value'),
        Input('year-input','value'),
        Input('livestock-or-asset-dropdown','value'),
        Input('species-dropdown','value'),
        Input('graph-type','data'),
    )
    def render_table(country,year,asset_type_value,species,graph_type):
        # Overriding asset type if crops
        asset_type = 'Crops' if species == 'Crops' else asset_type_value
        asset_type = 'Output' if species == 'Aquaculture' else asset_type
        
        # Wrapping items in list
        country = list() if country is None else list(country)
        
        # Filtering data with the menu values
        new_df = tevdata.df
        new_df = tevdata.filter_type(asset_type, new_df,None if graph_type == 'world' else 'All')
        new_df = tevdata.filter_species(species, new_df,None if graph_type == 'world' else 'All')
        if(graph_type=='world'):
            new_df = tevdata.filter_year(year, new_df)
        else:
            new_df = tevdata.filter_country(country, new_df,None if graph_type == 'world' else 'All')

        # Rendering the world plot
        cols = [{"name": i, "id": i,"hideable":True} for i in new_df.columns]
        cols[0] = {"name": "ID", "id": cols[0]["id"],"hideable":True}
        datatable = dash_table.DataTable(
            data=new_df.to_dict('records'),
            columns=cols,
            export_format="csv",
        )

        # Default message
        amsg = None
        if graph_type == 'world':
            if new_df.shape[0] == 0:
                amsg = ['No data avaliable for your selection.','warning']
            # if (country is None or (isinstance(country, list) and (len(country) > 1 or len(country) == 0))) and (prodsys is None or (isinstance(prodsys, list) and (len(prodsys) > 1 or len(prodsys) == 0))):
            #     amsg = ['Please choose 1 production system when graphing multiple countries.','danger']
        else:
            multidim = 0
            # summing multi dimensional data
            if len(country) != 1 or 'All' in country:
                multidim += 1
            if species is None or 'All' in species:
                multidim += 1
            if asset_type is None or 'All' in asset_type:
                multidim += 1

            if multidim > 1:
                amsg = ['You are trying to graph multi-dimensional data, please narrow your selection.','danger']

            if new_df.shape[0] == 0:
                amsg = ['No data avaliable for your selection.','warning']

            # if country is None or isinstance(country, str) or (isinstance(country, list) and len(country) < 2):
            #     amsg = ['You must select 2 countries when comparing pie charts.','danger']
            # elif (isinstance(country, list) and len(country) > 2):
            #     amsg = ['Only the first 2 countries selected will be used for the pie charts.','warning']

        return datatable,None if amsg is None else dbc.Alert([html.H5('Warning'),amsg[0]], color=amsg[1])

    ### Collapsing Datatable ###
    @dash_app.callback(
        Output('tab-section-table','style'),
        Output('tbl-btn-chevron','style'),
        Output('table-collapsed','data'),
        Input('table-collapse-button','n_clicks'),
        State('table-collapsed','data'),
    )
    def collapse_table(_a, collapsed):
        tabstyle = None
        chevronstyle = None

        if _a is None:
            return tabstyle,chevronstyle,collapsed
            
        if not collapsed:
            tabstyle = {'flex':'0'}
            chevronstyle = {'transform': 'rotate3d(1, 0, 0, 180deg)'}
            
        
        return tabstyle,chevronstyle,not collapsed


    ### Updating METADATA ###
    @dash_app.callback(
        Output('metadata-container','children'),
        Output('download-container','children'),
        Output('meta-type','data'),
        Input('meta-gbads-button','n_clicks'),
        Input('provenance-button','n_clicks'),
        Input('glossary-button','n_clicks'),
        Input('meta-source-dropdown','value'),
        State('meta-type','data'),
    )
    def update_meta(MetaButton,ProvButton,GlossButton,MetaValue,MetaType):        
        # Filtering data with the menu values
        pressed = callback_context.triggered[0]['prop_id'].split('.')[0]
        df = ''
        downloadButton = ''
        meta=MetaType

        if (pressed == 'meta-source-dropdown' and MetaType == 'meta') or pressed == 'meta-gbads-button' or pressed == '':
            meta = 'meta'
            df = pd.read_csv(METADATA_SOURCES[MetaValue]['METADATA'], names=['Col1', 'Col2'])
            req = requests.get(METADATA_SOURCES[MetaValue]['DOWNLOAD'])
            json_data = json.dumps(req.json(), indent=2, ensure_ascii=False).replace('#', '%23')
            downloadButton = html.A(
                href=f"data:text/json;charset=utf-8,{json_data}",
                children='Download Metadata',download=METADATA_SOURCES[MetaValue]['DOWNLOAD'].split('/')[-1],id='meta-download-button',className='download-button'
            )
        elif (pressed == 'meta-source-dropdown' and MetaType == 'pro') or pressed == 'provenance-button':
            meta = 'pro'
            with open(METADATA_SOURCES[MetaValue]['PROVENANCE']) as file:
                df = dcc.Markdown(file.readlines())
            return df,downloadButton,meta
        elif pressed == 'glossary-button':
            df = pd.read_csv(METADATA_OTHER['GLOSSARY']['CSV'], names=['Col1', 'Col2'])

        datatable = dash_table.DataTable(
            data=df.to_dict('records'),
            # Removing header
            css=[{'selector': 'tr:first-child','rule': 'display: none'}],
            # Adding hyperlinks
            columns=[
                {'name': 'Col1', 'id': 'Col1'},
                {'name': 'Col2', 'id': 'Col2', 'presentation': 'markdown'}
            ],
            # Styling
            style_cell={'textAlign': 'left'},
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
            },
            style_data_conditional=[
                {
                    'if': {
                        'column_id': 'Col1',
                    },
                    'fontWeight': 'bold'
                }
            ],
            cell_selectable=True,
        )
        return datatable,downloadButton,meta
