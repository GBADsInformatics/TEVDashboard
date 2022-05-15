import json
from logging import disable
import requests
import numpy as np
import pandas as pd
import math
import urllib.parse
import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from dash import dash_table
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
import json
from textwrap import dedent


PROFILE_KEY = 'profile'
JWT_PAYLOAD = 'jwt_payload'

stylesheet = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css'
    # dbc.themes.BOOTSTRAP
]

def init_dashboard(server):
            
    dash_app = dash.Dash(__name__,
        server=server,
        routes_pathname_prefix="/dash/",
        external_stylesheets=[
            # 'https://codepen.io/chriddyp/pen/bWLwgP.css',
            dbc.themes.BOOTSTRAP
        ],
    )
    # Setting active page
    dash_app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ])
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
    p = (person_dict["http://gbad.org/roles"])
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

    # Sidebar Callbacks
    # Callback to update the sidebar.
    @dash_app.callback(
        Output('left-button', 'children'), 
        Input('left-button', 'n_clicks')
    )
    def change_button_icon(n_clicks):
        if n_clicks%2 == 1:
            return ">"
        else:
            return "<"
    @dash_app.callback(
        Output('right-div', 'className'), 
        Input('left-button', 'n_clicks')
    )
    def extend_div(n_clicks):
        if n_clicks%2 == 1:
            return "options-right-open"
        else:
            return "options-right"
    @dash_app.callback(
        Output('left-div', 'className'), 
        Input('left-button', 'n_clicks')
    )
    def slide_div_in(n_clicks):
        if n_clicks%2 == 1:
            return "options-left-closed"
        else:
            return "options-left"

    # Callback to update the components in the bottom box.
    @dash_app.callback(
        Output('my-slider', 'className'),
        Input('tabs', 'value')
    )
    def hide_slider1(tabname):
        if (tabname == "tab-1"):
            return 'show m-m'
        else:
            return 'hide'
    @dash_app.callback(
        Output('my-slider-single', 'className'),
        Input('tabs', 'value')
    )
    def hide_slider2(tabname):
        if (tabname == "tab-2"):
            return 'show m-m'
        else:
            return 'hide'

    @dash_app.callback(
        Output('feedback-input', 'className'),
        Input('tabs', 'value')
    )
    def hide_slider3(tabname):
        if (tabname == "tab-3"):
            return 'show'
        else:
            return 'hide'
    
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