# GBADs Dashboard Template Layouts 
# This file includes all the layout components seen in the dashboard pages. This template 
# includes many of the components that you might require.

# IMPORTS
# These are the imports required for building a dashboard with visualizations and user 
# authentication.
from logging import PlaceHolder, disable
from pydoc import classname
import dash
from dash import dcc,html,dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate 
import pandas as pd
import numpy as np
import json
import plotly.express as px
from flask_app.plotlydash.TEVdata import *
# from dash_extensions.enrich import FileSystemStore

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


# Sky's defs in "biomass_dashboard.py"
# fss = FileSystemStore(cache_dir='TEV_cache')


# TAB STYLING
# This is the styling that is applied to the selected tab.
selectedTabStyle = {
    'borderTop': '1px white',
    'borderBottom': '1px white',
    'borderLeft': '1px white',
    'borderRight': '1px white',
    'background-color': '#f6f6f6d1',
    'box-shadow': '1px 1px 0px white',
    'color': 'orange',
    'fontWeight': 'bold'
}

# PAGE LAYOUT
# All the components for a page will be put here in this HTML div and will be used as the layout 
# for this dashboard template.
page_1 = html.Div([
    html.Div([
        html.Img(src=GBADSLOGOB, className="header-logo"),
        html.Div([html.H1('Economic Value of Livestock', className="header-title")], className="header-title-div"),
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
                        html.Div(
                            className="f-h-scroll-div",
                            children=[
                            html.Div(
                                className='tab-section-container',
                                children=[
                                html.Div(
                                    id='tab-section-loading',
                                    className='tab-section-container-div',
                                    children=[
                                        html.Div([
                                            html.P(
                                                'This dashboard provides estimates of the global economic value of livestock and aquatic farmed animals, with a focus on the value of live animals and primary production outputs (e.g., meat, eggs, milk) from 1996-present.',
                                                style={'color':'#000','margin':'0'}
                                            )
                                        ],className='tab-section'),
                                        html.Div(
                                            className='tab-section tab-section-table',
                                            id='tab-section-table',
                                            children=[
                                                dcc.Loading(
                                                    id='data-table-parent',
                                                    parent_style={'height':'100%','width':'100%','overflow':'scroll'},
                                                    type='circle',
                                                    children=[html.P('Please select appropriate dropdown options.')]
                                                ),
                                            ],
                                        ),
                                        html.Div(
                                            html.I(className="bi bi-chevron-up",id='tbl-btn-chevron'),
                                            id='table-collapse-button',
                                            className='tab-section table-collapse-button',
                                        ),
                                        html.Div([
                                            html.Div([
                                                html.Div([
                                                    html.Div([
                                                        html.H4(children="Graph Type"),
                                                        
                                                        html.Div([
                                                            html.Img(src="https://i.imgur.com/6z8MNOr.png", className="graph-type-image", id='area-graph' , n_clicks=0),
                                                            html.Hr(style={'width':'80%'}),
                                                            html.Img(src="https://i.imgur.com/kntGlf2.png", className="graph-type-image", id='world-map', n_clicks=0)
                                                        ],
                                                        className='graph-type-image-container',
                                                        style={'color':'#000'}),

                                                    ], className='graph-section-type'),
                                                    html.Div([
                                                        html.H4(children="Graph Options"), 
                                                        
                                                        html.Div(
                                                            id='year-container',
                                                            children=[],
                                                        ),

                                                        # Geography dropdown
                                                        html.H5(id="first-dropdown-title",children="Geography",style={"margin":"0.4rem 0 0.2rem 0"}),
                                                        dcc.Dropdown(
                                                            # className="graph-options-dropdown-TEV",
                                                            id='country-dropdown',
                                                            multi=True,
                                                            options=[],
                                                            value=['Indonesia']
                                                        ),

                                                        #Species
                                                        html.H5(children="Species",style={"margin":"0.4rem 0 0.2rem 0"}), 
                                                        dcc.Dropdown(
                                                            # className="graph-options-dropdown-TEV",
                                                            id="species-dropdown",
                                                            options=[],
                                                            clearable=True,
                                                            multi=True,
                                                            style={"color": "black"},
                                                            value=["Aquaculture", "Cattle", "Chicken", "Crops"]
                                                        ),

                                                        #Livestock or Asset dropdown
                                                        html.Div([
                                                                html.H5(children="Value Type",style={"margin":"0.4rem 0.5rem 0.2rem 0"}), 
                                                                html.Div([
                                                                        html.I(className="bi bi-info-circle-fill me-2"),
                                                                        html.Span([
                                                                                "LIVE ANIMALS: Asset value of living animals.",
                                                                                html.Br(),
                                                                                "OUTPUT: Value generated by products of an animal.",
                                                                                html.Br(),
                                                                                "TOTAL: Live animals + output.",
                                                                                html.Br(),
                                                                                "ALL TYPES: Graph all 3 types",
                                                                            ],
                                                                            className="ttooltiptext",
                                                                        ),
                                                                    ],
                                                                    className="ttooltip",
                                                                ),
                                                            ],    
                                                            className="value-container",
                                                        ),
                                                        dcc.Dropdown(
                                                            # className="graph-options-dropdown-TEV",
                                                            id="livestock-or-asset-dropdown",
                                                            options=[],
                                                            clearable=False,
                                                            style={"color": "black"},
                                                            value="Total"
                                                        ),


                                                        #Log Transform dropdown
                                                        html.H5(children="Log Transform",id="log-dropdown-title",style={"margin":"0.4rem 0 0.2rem 0"}), 
                                                        dcc.Dropdown(
                                                            id="log-dropdown",
                                                            options=['None', 'Log'],
                                                            value='Log',
                                                            clearable=False,
                                                            style={"color": "black"},
                                                        ),

                                                        #Colour By
                                                        # html.H5(children="Colour By",style={"margin":"0.4rem 0 0.2rem 0"},id='colour-by-title'), 
                                                        # dcc.Dropdown(
                                                        #     # className="graph-options-dropdown-TEV",
                                                        #     id="colour-dropdown",
                                                        #     options=[
                                                        #         'Auto',
                                                        #         'Country',
                                                        #         'Species',
                                                        #         'Type',
                                                        #     ],
                                                        #     clearable=False,
                                                        #     value='Auto',
                                                        #     style={"color": "black"},
                                                        # ),

                                                    ], className='graph-section-options'),
                                                ], className='graph-section-left-top'),
                                                html.Div([
                                                    html.Div(
                                                        id='alert-container',
                                                        children=[],
                                                        style={'margin-top':'1rem'}
                                                    ),
                                                ], className='graph-section-left-bottom'),
                                            ],className='graph-section-left'),
                                            dcc.Loading(
                                                id='main-graph-parent',
                                                type='circle',
                                                parent_className='graph-section-right',
                                                children=[html.P('Please select appropriate dropdown options.')]
                                            ),
                                        ],className='tab-section graph-section')
                                    ]
                                )
                            ]),
                        ]),
                    ],  
                    className='cattabs',
                    selected_style=selectedTabStyle,
                ),
                dcc.Tab(
                    label='Metadata & API', 
                    className='cattabs', 
                    selected_style=selectedTabStyle,
                    children=[
                        html.Div(
                            className="f-h-scroll-div",
                            children=[
                                html.Div(
                                    className='tab-section-container',
                                    children=[
                                        html.Div(
                                            id='tab-section-loading',
                                            className='tab-section-container-div',
                                            children=[
                                                html.Div([
                                                    html.P(
                                                        'GBADs Informatics metadata provides information about data presented in the \'Data and Graphs\' tab. Metadata is provided for data that is used as inputs to the model used to produce data outputs. Metadata is provided for output data including provenance information and methodology for the model.',
                                                        style={'color':'#000','margin':'0'}
                                                    )
                                                ],className='tab-section'),
                                                html.Div(
                                                    className='meta-section-wrapper',
                                                    children=[
                                                        html.Div(
                                                            className='meta-section',
                                                            children=[
                                                                html.Div(
                                                                    className='meta-section-left tab-section',
                                                                    id='meta-left',
                                                                    children=[
                                                                        html.H5(children="Data Source",style={"text-align":"center"}), 
                                                                        html.Div(
                                                                            className='meta-gbads-source',
                                                                            id='gbads-source',
                                                                            children=[
                                                                                dcc.Dropdown(
                                                                                    className="meta-source-button meta-source-dropdown",
                                                                                    id="meta-source-dropdown",
                                                                                    options=[*METADATA_SOURCES],
                                                                                    value=[*METADATA_SOURCES][0],
                                                                                    clearable=False,
                                                                                    style={"color": "black"},
                                                                                ),
                                                                                html.P(
                                                                                    'GBADs Metadata',
                                                                                    className='meta-source-button meta-gbads-button',
                                                                                    id='meta-gbads-button'
                                                                                ),
                                                                                html.P(
                                                                                    'Provenance',
                                                                                    className='meta-source-button provenance-button',
                                                                                    id='provenance-button',
                                                                                ),
                                                                            ]
                                                                        ),
                                                                        html.Div(
                                                                            className='meta-source-button',
                                                                            id='glossary-button',
                                                                            children=[
                                                                                'Metadata Glossary'
                                                                                # html.Div(),
                                                                            ]
                                                                        ),
                                                                    ]
                                                                ),
                                                                html.Div([
                                                                    html.Div(
                                                                        children=[
                                                                            html.H5(children='Metadata',style={"text-align":"center",'height':'2rem'}), 
                                                                            html.Div(
                                                                                children=[],
                                                                                id='download-container',
                                                                                className='download-container',
                                                                            ),
                                                                        ],
                                                                        style={'position':'relative'}
                                                                    ),
                                                                    html.Div(
                                                                        dcc.Loading(
                                                                            # parent_className='loading-wrapper',
                                                                            id='metadata-container',
                                                                            type='circle',
                                                                            children=[
                                                                                'Metadata shows here'
                                                                            ],
                                                                        ),
                                                                        className='meta-data-container',
                                                                    ),
                                                                ],className='meta-section-right tab-section'),
                                                            ]
                                                        ),
                                                    ]
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ]
                        ),
                    ],  
                ),
            ]),
        ], className="r tab-panel"),
    ],className='mid'),
        
    # Storing data in the session. Data gets deleted once tab is closed
    dcc.Store(id='graph-type', storage_type='memory', data='line'),
    dcc.Store(id='meta-type', storage_type='memory', data='meta'),
    dcc.Store(id='table-collapsed', storage_type='memory', data=False),

], className="main-div")
