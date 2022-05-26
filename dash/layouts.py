# GBADs Dashboard Template Layouts 
# This file includes all the layout components seen in the dashboard pages. This template 
# includes many of the components that you might require.

# IMPORTS
# These are the imports required for building a dashboard with visualizations and user 
# authentication.
from logging import PlaceHolder, disable
import dash
from dash import dcc
from dash.html.H4 import H4
import dash_bootstrap_components as dbc
from dash import html
from dash import dash_table
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate 
import pandas as pd
import numpy as np
import json
from textwrap import dedent
from os import environ as env


#  IMAGES
# Example images set for the dashboard template, used for logos of the company/entity that is
# showcasing the data visualization. Add more by adding local files to \assets or by image URL.
GBADSLOGOB = "https://i0.wp.com/animalhealthmetrics.org/wp-content/uploads/2019/10/GBADs-LOGO-Black-sm.png"
GBADSLOGOW = "https://i0.wp.com/animalhealthmetrics.org/wp-content/uploads/2019/10/GBADs-LOGO-White-sm.png"


# SLIDER VALUES
# Year list that is used by the sliders that are shown at the bottom of the template, currently hard  
# coded but the values can be dynamic by being processed from a file.
year_list = []         # change this value
y_value = 1999           # change this value
y_max = 2021               # change this value
while y_value <= y_max:
     year_list.append(y_value)
     y_value += 1


# DROPDOWNS 
# Generic dropdown menu, can hold different values by adding content to the options array/list.
country_dropdown = dcc.Dropdown(
    id='faostat-country-dropdown-menu',
    multi=True,
    options=[],
)


# TAB STYLING
# This is the styling that is applied to the selected tab.
selectedTabStyle = {
    'border': '3px solid white',
    'backgroundColor': 'white',
    'color': 'black'
}

# Where to get the table dataset from
ds = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

# PAGE LAYOUT
# All the components for a page will be put here in this HTML div and will be used as the layout 
# for this dashboard template.
page_1 = html.Div([
    html.Div([
        html.Img(src=GBADSLOGOW, className="header-logo"),
        html.Div([html.H1('Total Economic Value of Livestock', className="header-title")], className="header-title-div"),
        # dbc.Button("Login", id="login-button", href=env.get("AUTH0_LOGIN"), style={'margin-top': '10px', 'margin-right':'10px', 'float': 'right'}),
        # dbc.Button("Logout", id="logout-button", href=env.get("AUTH0_LOGOUT"), style={'margin-top': '10px', 'margin-right':'10px', 'float': 'right', 'display':'none'}),
    ],className='header-section'),
    
    html.Div([
        html.Div([
            # This is the tabs component. It holds all the pages for the tabs. Add more tabs and change the 
            # tab contents here.
            dcc.Tabs(
                id='tabs',
                children=[
                dcc.Tab(
                    label='Graphs & Data', 
                    children=[
                        html.Div([
                            html.Div([
                                dcc.Loading(
                                    id='tab-section-loading',
                                    type='circle',
                                    parent_className='tab-section-container-div',
                                    children=[
                                        html.Div([
                                            html.P(
                                                'This dashboard provides estimates of the global economic value of livestock and aquatic farmed animals, with a focus on the value of live animals and primary production outputs (e.g., meat, eggs, milk) from 1996- present.',
                                                style={'color':'#000'}
                                            )
                                        ],className='tab-section'),
                                        html.Div([
                                            dash_table.DataTable(ds.to_dict('records'), [{"name": i, "id": i} for i in ds.columns])
                                        ],
                                        className='tab-section',
                                        style={'color':'#000'}),
                                        html.Div([
                                            html.Div([
                                                html.Div([
                                                    html.Div([
                                                        html.H3(children="Graph Type"),
                                                        
                                                        html.Div([
                                                            html.Img(src="https://i.imgur.com/6z8MNOr.png", className="header-logo"),
                                                            html.Hr(style={'width':'80%'}),
                                                            html.Img(src="https://i.imgur.com/kntGlf2.png", className="header-logo")
                                                        ],
                                                        className='graph-type-image-container',
                                                        style={'color':'#000'}),

                                                    ], className='graph-section-type'),
                                                    html.Div([
                                                        html.H3(children="Graph Options"), 

                                                        # Geography dropdown
                                                        html.H5(children="Geography"),                                                 
                                                        dcc.Dropdown(
                                                            className="graph-options-dropdown-TEV",
                                                            id="geography-dropdown",
                                                            options=[
                                                                {'label': 'some-label', 'value': 'some-value'},
                                                                {'label': 'some-label', 'value': 'some-value'},
                                                                {'label': 'some-label', 'value': 'some-value'}
                                                            ],
                                                            value='California',
                                                            style={"color": "black"},
                                                        ),

                                                        #Livestock or Asset dropdown
                                                        html.H5(children="Livestock or Asset"), 
                                                        dcc.Dropdown(
                                                            className="graph-options-dropdown-TEV",
                                                            id="livestock-or-asset-dropdown",
                                                            options=[
                                                                {'label': 'some-label', 'value': 'some-value'},
                                                                {'label': 'some-label', 'value': 'some-value'},
                                                                {'label': 'some-label', 'value': 'some-value'}
                                                            ],
                                                            value='Chickens',
                                                            style={"color": "black"},
                                                        ),

                                                        #Species
                                                        html.H5(children="Species"), 
                                                        dcc.Dropdown(
                                                            className="graph-options-dropdown-TEV",
                                                            id="species-dropdown",
                                                            options=[
                                                                {'label': 'some-label', 'value': 'some-value'},
                                                                {'label': 'some-label', 'value': 'some-value'},
                                                                {'label': 'some-label', 'value': 'some-value'}
                                                            ],
                                                            value='Priority Species',
                                                            style={"color": "black"},
                                                        ),

                                                        #Value
                                                        html.H5(children="Value"), 
                                                        dcc.Dropdown(
                                                            className="graph-options-dropdown-TEV",
                                                            id="value-dropdown",
                                                            options=[
                                                                {'label': 'some-label', 'value': 'some-value'},
                                                                {'label': 'some-label', 'value': 'some-value'},
                                                                {'label': 'some-label', 'value': 'some-value'}
                                                            ],
                                                            value='A value',
                                                            style={"color": "black"},
                                                        ),

                                                    ], className='graph-section-options'),
                                                ], className='graph-section-left-top'),
                                                html.Div([html.P('Data from FAOSTAT xxxxx. Retrieved August 04, 2021 from [url]',style={'color':'#000','margin':'0'}),], className='graph-section-left-bottom'),
                                            ],className='graph-section-left'),
                                            html.Div([
                                                dcc.Graph(id='faostat-choromap-2', className='main-graph-size')
                                            ],className='graph-section-right'),
                                        ],className='tab-section graph-section')
                                    ],
                                )
                            ], className='tab-section-container'),
                        ], className="f-h-scroll-div"),
                    ],  
                    className='cattabs',
                    selected_style=selectedTabStyle
                ),
                dcc.Tab(
                    label='Metadata & API', 
                    children=[
                        html.Div([
                            html.Div([
                                dcc.Loading(
                                    # parent_className='loading-wrapper',
                                    id='faostat-choro-map-loading-2',
                                    children=[dcc.Graph(id='faostat-choromap-2', className='graph-size')],
                                    type='circle'
                                ),
                            ]),
                        ], className="f-h-scroll-div"),
                    ],  
                    className='cattabs', 
                    selected_style=selectedTabStyle
                ),
            ]),
        ], className="r tab-panel"),
    ],className='mid'),
        
    html.Div([
        # Placeholder to store user selection of options and display them once all the necessary 
        # information has been given
        dcc.Store(id='species-selected', data='Chickens'),
    ], style={'display': 'none'}),
], className="main-div")

