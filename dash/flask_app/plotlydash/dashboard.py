import json
from logging import disable
import requests
import numpy as np
import pandas as pd
import math
import urllib.parse
import dash
from dash import dcc,html,dash_table
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
from .TEVdata import TEVdata

PROFILE_KEY = 'profile'
JWT_PAYLOAD = 'jwt_payload'

stylesheet = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css'
    # dbc.themes.BOOTSTRAP
]

# Where to get the table dataset from
tevdata = TEVdata('datasets/20220603_informatics_tev_data.csv', 'line')


def init_dashboard(server):
            
    dash_app = dash.Dash(__name__,
        server=server,
        title='TEV Dashboard',
        routes_pathname_prefix="/dash/",
        external_stylesheets=[
            # 'https://codepen.io/chriddyp/pen/bWLwgP.css',
            dbc.themes.BOOTSTRAP
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

print(isLoggedIn)
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
        Output('species-dropdown','options'),
        Input('area-graph','n_clicks'),
        Input('world-map','n_clicks'),
    )
    def update_graph_type(_a,_b,):
        ctx = dash.callback_context
        if not ctx.triggered:
            button_id = 'No clicks'
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id=="area-graph" or button_id=='No clicks':
            tevdata.graph_type = 'line'
            return 'Geography',tevdata.countries,{'display':'block'},{'display':'none'},tevdata.min_year,tevdata.max_year,tevdata.types,tevdata.species
        else:
            tevdata.graph_type = 'world'
            return 'Year',tevdata.countries,{'display':'none'},{'display':'block'},tevdata.min_year,tevdata.max_year,tevdata.types,tevdata.species

    ### Updating Figure ###
    @dash_app.callback(
        Output('main-graph','figure'),
        Input('area-graph','n_clicks'),
        Input('world-map','n_clicks'),
        Input('country-dropdown','value'),
        Input('year-input','value'),
        Input('livestock-or-asset-dropdown','value'),
        Input('species-dropdown','value'),
    )
    def render_figure(_a,_b,country,year,asset_type,species):
        new_df = tevdata.df
        new_df = tevdata.filter_type(asset_type, new_df)
        new_df = tevdata.filter_species(species, new_df)
        if(tevdata.graph_type=='line'):
            new_df = tevdata.filter_country(country, new_df)

        color_by = 'category'
        if asset_type is None: color_by = 'type'
        if country is None: color_by = 'iso3_code'

        if(tevdata.graph_type=='world'):
            fig_world= go.Figure(go.Scattergeo())
            fig_world.update_geos(
                resolution=50,
                showcoastlines=True, coastlinecolor="RebeccaPurple",
                showland=True, landcolor="LightGreen",
                showocean=True, oceancolor="LightBlue",
                showlakes=True, lakecolor="Blue",
                showrivers=True, rivercolor="Blue"
            )
            fig_world.update_layout(autosize = True, margin={"r":0,"t":0,"l":0,"b":0})
            return fig_world
        else:
            fig = px.line(new_df, x='year',y='value',color=color_by,title='Economic Value Over Time')
            fig.layout.autosize = True
            return fig

