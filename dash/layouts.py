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
import plotly.express as px
from textwrap import dedent
from os import environ as env
from dash_extensions.enrich import DashProxy, Output, Input, State, ServersideOutput, html, dcc, ServersideOutputTransform, FileSystemStore

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

# Sky's defs in "biomass_dashboard.py"
fss = FileSystemStore(cache_dir='TEV_cache')
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = DashProxy(transforms=[ServersideOutputTransform(backend=fss)], external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

# TAB STYLING
# This is the styling that is applied to the selected tab.
selectedTabStyle = {
    'border': '3px solid white',
    'backgroundColor': 'white',
    'color': 'black'
}

# Where to get the table dataset from
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')
fig = px.area(df, x = 'Number of Solar Plants', y = 'Average MW Per Plant', title='Solar CSV')

# PAGE LAYOUT
# All the components for a page will be put here in this HTML div and will be used as the layout 
# for this dashboard template.
page_1 = html.Div([
    html.Div([
        html.Img(src=GBADSLOGOW, className="top"),
        html.Div([html.H1('Total Economic Value of Livestock')], style={'display': 'inline-block', 'margin-left': '35%'}),
        # dbc.Button("Login", id="login-button", href=env.get("AUTH0_LOGIN"), style={'margin-top': '10px', 'margin-right':'10px', 'float': 'right'}),
        # dbc.Button("Logout", id="logout-button", href=env.get("AUTH0_LOGOUT"), style={'margin-top': '10px', 'margin-right':'10px', 'float': 'right', 'display':'none'}),
    ]),
    
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
                                            dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])
                                        ],
                                        className='tab-section',
                                        style={'color':'#000'}),
                                        html.Div([
                                            html.Div([
                                                html.Div([
                                                    html.Div([
                                                        html.H3(children="Graph Type"),
                                                        
                                                        html.Div([
                                                            html.Img(src="https://i.imgur.com/6z8MNOr.png", className="top", id='area-graph', n_clicks=0),
                                                            html.Hr(style={'width':'80%'}),
                                                            html.Img(src="https://i.imgur.com/kntGlf2.png", className="top", id='map-map', n_clicks=0)
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
                                                dcc.Graph(id='faostat-choromap-2', className='main-graph-size', figure=fig)
                                            ],className='graph-section-right', id="main-graph"),
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

@app.callback(
    Output('main-graph', 'children'),
    [Input('area-graph', 'n_clicks')],
    [State('faostat-choro-map-loading-2', 'type')]
)
def render_content(n_clicks, type):
    if n_clicks > 0:
        return html.Div([
            html.H3('Graph 1', style={"backgroundColor":"white","color":"black"}),
            dcc.Graph(
                figure=dict(
                    data=[dict(
                        x=[1, 2, 3],
                        y=[3, 1, 2],
                        type='bar'
                    )]
                )
            )
        ],style={"backgroundColor":"white"})
    else:
        return None

# @app.callback(
#     Output(component_id='faostat-choro-map-loading-2', component_property='type'),
#     [Input(component_id='area-graph', component_property='n_clicks_timestamp')],
#     [State(component_id='faostat-choro-map-loading-2', component_property='type')]
# )
# def update_graph(click, type):
#     if not click: raise PreventUpdate
#     return "Area Plot"
