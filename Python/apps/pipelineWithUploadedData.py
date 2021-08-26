import dash
from dash_bootstrap_components._components.Row import Row
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import pathlib
from app import app
import os
import base64
import datetime
import io
import pipeline

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

# get all the newick files produced 
tree_path = os.listdir()
tree_files = []
for item in tree_path:
    if item.endswith("_newick"):
        tree_files.append(item)

#-------------------------------------------
layout = dbc.Container([
    html.H1('Phylogenetic Tree', style={"textAlign": "center"}),  #title
    
    # the first row
    dbc.Row([
        dbc.Col([
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select .fasta Files')
                ]),
                style={
                    'width': '99%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                # Allow multiple files to be uploaded
                multiple=True
            ),
        ],# width={'size':3, 'offset':1, 'order':1},
           xs=12, sm=12, md=12, lg=10, xl=10
        ),
    ], no_gutters=True, justify='around'),  # Horizontal:start,center,end,between,around 

    # The second row
     dbc.Row([

        dbc.Col([
            html.Div([
                html.H3("Bootstrap value threshold"),
                dcc.Slider(id='BootstrapThreshold-slider',
                            min=0,  
                            max=100,
                            step=0.1,
                            marks={
                                0: {'label':'0.0%','style': {'color': '#77b0b1'}},
                                25: {'label':'25.0%','style': {'color': '#77b0b1'}},
                                50: {'label':'50.0%','style': {'color': '#77b0b1'}},
                                75: {'label':'75.0%','style': {'color': '#77b0b1'}},
                                100: {'label':'100.0%','style': {'color': '#77b0b1'}}},
                            value=10),
                html.Div(id='BootstrapThreshold-slider-output-container')        
            ]),
        ], #width={'size':5, 'offset':0, 'order':2},
           xs=12, sm=12, md=12, lg=5, xl=5
        ),

        dbc.Col([
            html.Div([
                html.H3("Robinson and Foulds distance threshold"),
                dcc.Slider(id='RF-distanceThreshold-slider',
                            min=0,
                            max=100,
                            step=0.1,
                            marks={
                                0: {'label':'0.0%', 'style': {'color': '#77b0b1'}},
                                25: {'label':'25.0%', 'style': {'color': '#77b0b1'}},
                                50: {'label':'50.0%', 'style': {'color': '#77b0b1'}},
                                75: {'label':'75.0%', 'style': {'color': '#77b0b1'}},
                                100: {'label':'100.0%','style': {'color': '#77b0b1'}}},
                            value=10),
                html.Div(id='RFThreshold-slider-output-container'),       
            ]),
            ], #width={'size':5, 'offset':0, 'order':2},
            xs=12, sm=12, md=12, lg=5, xl=5
            ),
    ], no_gutters=True, justify='around'),  # Horizontal:start,center,end,between,around
    
    # for sliding window size & step size 
    dbc.Row([

        dbc.Col([
            html.Div([
                html.H3("Sliding Window Size"),
                dcc.Input(id = "input_windowSize1", type = "number", min = 0, max = 5000,
                    placeholder = "Enter Sliding Window Size", 
                    style= {'width': '65%','marginRight':'20px'}), 
                html.Div(id='WindowSize-output-container1')        
                    ]),

        ],# width={'size':3, 'offset':1, 'order':1},
           xs=12, sm=12, md=12, lg=5, xl=5
        ),

        dbc.Col([
            html.Div([
                html.H3("Step Size"),
                dcc.Input(id = "input_stepSize1", type = "number", min = 0, max = 5000, 
                    placeholder = "Enter Step Size", 
                    style= {'width': '65%','marginRight':'20px'}),
                html.Div(id='StepSize-output-container1')        
                    ]),
        ],# width={'size':3, 'offset':1, 'order':1},
           xs=12, sm=12, md=12, lg=5, xl=5
        ),
    ], no_gutters=True, justify='around'),  # Horizontal:start,center,end,between,around 

    # select the files of reference tree
    dbc.Row([
            dbc.Col([
                html.Br(),
                html.Hr(),
                html.H3("Select the file(s) of reference trees"),
                dcc.Checklist(id = 'reference_trees1',
                            options =[{'label': x, 'value': x} for x in tree_files],
                            labelStyle={'display': 'inline-block','marginRight':'20px'})
            ],# width={'size':3, 'offset':1, 'order':1},
            xs=12, sm=12, md=12, lg=10, xl=10
            ),
        ], no_gutters=True, justify='around'),

    dbc.Row([
        dbc.Col([
            #html.Br(),
            html.Hr(),
            #html.Br(),
            html.Div(id='output-fasta'),
        ],# width={'size':3, 'offset':1, 'order':1},
           xs=12, sm=12, md=12, lg=10, xl=10
        ),
    ], no_gutters=True, justify='around'),  # Horizontal:start,center,end,between,around 
    
    #submit button
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.Button(id="submit-button", children="Submit"),
            html.Br(),
            html.Hr(),
        ],# width={'size':3, 'offset':1, 'order':1},
           xs=12, sm=12, md=12, lg=10, xl=10
        ),
    ], no_gutters=True, justify='around'),

    # for output of pipeline
    dbc.Row([
            dbc.Col([
                html.Div(id='output-container'),
            ],xs=12, sm=12, md=12, lg=10, xl=10),

         ],no_gutters=True, justify='around'),
   
    
], fluid=True)



#-------------------------------------------------
# view the value chosen
@app.callback(
    dash.dependencies.Output('BootstrapThreshold-slider-output-container', 'children'),
    [dash.dependencies.Input('BootstrapThreshold-slider', 'value')])
def update_output(value):
    return 'You have selected {:0.1f}%'.format(value)

@app.callback(
    dash.dependencies.Output('RFThreshold-slider-output-container', 'children'),
    [dash.dependencies.Input('RF-distanceThreshold-slider', 'value')])
def update_output(value):
    return 'You have selected {:0.1f}%'.format(value)

# callback for sliding window siza & step size; view the value chosen
@app.callback(
    dash.dependencies.Output('WindowSize-output-container1', 'children'),
    [dash.dependencies.Input('input_windowSize1', 'value')])
def update_output(value):
    return 'You have selected {}'.format(value)

@app.callback(
    dash.dependencies.Output('StepSize-output-container1', 'children'),
    [dash.dependencies.Input('input_stepSize1', 'value')])
def update_output(value):
    return 'You have selected {}'.format(value)

# get the contens of uploaded files    

def parse_fasta_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'fasta' in filename:
            # Assume that the user uploaded a fasta file
            seq_upload = decoded.decode('utf-8')
            return html.Div([
                        dcc.Markdown('You have uploades file(s):  **{}**'.format(filename)),
                        #html.H6(datetime.datetime.fromtimestamp(date)),
                        #html.Small(seq_upload),
                        # For debugging, display the raw contents provided by the web browser
                        #html.Div('Raw Content'),
                        #html.Pre(contents[0:200] + '...', style={
                         #   'whiteSpace': 'pre-wrap',
                         #   'wordBreak': 'break-all'
                        #})
                    ])
        else:
            # Assume that the user uploaded other files
            return html.Div([
                'Please upload a fasta file.'
        ])
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.' 
        ])

    
#callback for uploaded data

@app.callback(Output('output-fasta', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_fasta_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


